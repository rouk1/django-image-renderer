#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import uuid
from io import BytesIO

from PIL import Image, ImageFile
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from picklefield.fields import PickledObjectField

# be sure to open image even if
# IOError at /renderer/masterimage/
# image file is truncated (50 bytes not processed)
ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGE_DIRECTORY = 'img'


def get_unique_file_name(instance, filename):
    filename, ext = os.path.splitext(filename)
    return '%s/%s%s' % (IMAGE_DIRECTORY, uuid.uuid4(), ext)


class MasterImage(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    master_width = models.PositiveIntegerField(editable=False, null=True)
    master_height = models.PositiveIntegerField(editable=False, null=True)
    master = models.ImageField(
        upload_to=get_unique_file_name,
        width_field='master_width',
        height_field='master_height'
    )
    alternate_text = models.CharField(max_length=256, blank=True)
    renditions = PickledObjectField(blank=True, editable=False)

    def __unicode__(self):
        if self.alternate_text:
            return self.alternate_text
        return 'master image'

    def get_master_url(self):
        '''return master image url'''
        return self.master.url

    def get_rendition_size(self, width=0, height=0):
        '''returns real rendition URL'''
        if width == 0 and height == 0:
            return (self.master_width, self.master_height)

        target_width = int(width)
        target_height = int(height)

        ratio = self.master_width / float(self.master_height)
        if target_height == 0 and target_width != 0:
            target_height = int(target_width / ratio)

        if target_height != 0 and target_width == 0:
            target_width = int(target_height * ratio)

        return target_width, target_height

    def get_rendition_url(self, width=0, height=0):
        '''get the rendition URL for a specified size

        if the renditions does not exists it will be created
        '''
        if width == 0 and height == 0:
            return self.get_master_url()

        target_width, target_height = self.get_rendition_size(width, height)

        key = '%sx%s' % (target_width, target_height)
        if not self.renditions:
            self.renditions = {}
        rendition_name = self.renditions.get(key, False)
        if not rendition_name:
            rendition_name = self.make_rendition(target_width, target_height)
        return default_storage.url(rendition_name)

    def get_master_filename(self):
        '''get master file filename'''
        return os.path.basename(self.master.name)

    def delete_all_renditions(self):
        '''delete all renditions and rendition dict'''
        if self.renditions:
            for r in self.renditions.values():
                default_storage.delete(r)
            self.renditions = {}

    def make_rendition(self, width, height):
        '''build a rendition

        0 x 0 -> will give master URL
        only width -> will make a renditions with master's aspect ratio
        width x height -> will make an image potentialy cropped
        '''
        image = Image.open(self.master)
        format = image.format

        target_w = float(width)
        target_h = float(height)

        if (target_w == 0):
            target_w = self.master_width

        if (target_h == 0):
            target_h = self.master_height

        rendition_key = '%dx%d' % (target_w, target_h)

        if rendition_key in self.renditions:
            return self.renditions[rendition_key]

        if (target_w != self.master_width or target_h != self.master_height):
            r = target_w / target_h
            R = float(self.master_width) / self.master_height
            if r != R:
                if r > R:
                    crop_w = self.master_width
                    crop_h = crop_w / r
                    x = 0
                    y = int(self.master_height - crop_h) >> 1
                else:
                    crop_h = self.master_height
                    crop_w = crop_h * r
                    x = int(self.master_width - crop_w) >> 1
                    y = 0
                image = image.crop((x, y, int(crop_w + x), int(crop_h + y)))

            image.thumbnail((int(target_w), int(target_h)), Image.ANTIALIAS)

            filename, ext = os.path.splitext(self.get_master_filename())
            rendition_name = '%s/%s_%s%s' % (
                IMAGE_DIRECTORY,
                filename,
                rendition_key,
                ext
            )
            fd = BytesIO()
            image.save(fd, format)
            default_storage.save(rendition_name, fd)

            self.renditions[rendition_key] = rendition_name
            self.save()

            return rendition_name

        return self.master.name


@receiver(pre_save, sender=MasterImage)
def delete_renditions_if_master_has_changed(sender, instance, **kwargs):
    '''if master file as changed delete all renditions'''
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new, so field hasn't technically changed.
    else:
        if not obj.master == instance.master:  # Field has changed
            obj.master.delete(save=False)
            instance.delete_all_renditions()


@receiver(post_delete, sender=MasterImage)
def photo_post_delete_handler(sender, **kwargs):
    '''delete image when rows is gone from database'''
    instance = kwargs.get('instance')
    instance.master.delete(save=False)
    instance.delete_all_renditions()
