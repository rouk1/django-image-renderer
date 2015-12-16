#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from renderer.models import MasterImage
from renderer.templatetags.renderer import rendition_url, rendition


def create_superuser():
    username = 'admin'
    password = '123456'

    User.objects.create_superuser(username, 'a@a.fr', password)
    return username, password


def make_image():
    image_file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
    image.save(image_file, format='png')
    image_file.seek(0)
    return image_file


def create_image():
    image_file = make_image()
    master_image = MasterImage(
        master=ContentFile(image_file.read(), 'test-image.png'),
        alternate_text='test'
    )
    master_image.save()

    return master_image


class RendererTest(TestCase):
    def test_create(self):
        master_image = create_image()
        self.assertTrue(MasterImage.objects.count() > 0)
        self.assertTrue(len(master_image.get_master_url()) > 0)
        self.assertTrue('test' not in master_image.get_master_filename())
        master_image.delete()

    def test_rendition(self):
        master_image = create_image()
        # FIXME force reopen the file
        # why should I do that ?
        master_image.master.open()
        master_image.get_rendition_url(40, 40)
        self.assertEqual(1, len(master_image.renditions))
        master_image.delete()

    def test_admin_pages(self):
        username, password = create_superuser()
        master_image = create_image()

        c = Client()
        c.login(username=username, password=password)

        r = c.get(reverse('admin:renderer_masterimage_changelist'))
        self.assertEqual(r.status_code, 200, (
            'cant access changelist'
        ))

        r = c.get(reverse('admin:renderer_masterimage_add'))
        self.assertEqual(r.status_code, 200, (
            'cant access add page'
        ))

        r = c.get(reverse('admin:renderer_masterimage_change', args=(master_image.pk,)))
        self.assertEqual(r.status_code, 200, (
            'cant access change page'
        ))
        master_image.delete()

    def test_views(self):
        master_image = create_image()

        c = Client()

        r = c.get(reverse('renderer:get_rendition_url', args=(master_image.pk, 0, 0)))
        self.assertEqual(r.status_code, 200, (
            'cant get_rendition_url for rendition 0x0'
        ))

        r = c.get(reverse('renderer:get_rendition_url', args=(master_image.pk, 0, 10)))
        self.assertEqual(r.status_code, 200, (
            'cant get_rendition_url for rendition 0x10'
        ))

        r = c.get(reverse('renderer:get_rendition_url', args=(master_image.pk, 10, 10)))
        self.assertEqual(r.status_code, 200, (
            'cant get_rendition_url for rendition 10x10'
        ))

        r = c.get(reverse('renderer:get_master_url', args=(master_image.pk,)))
        self.assertEqual(r.status_code, 200, (
            'cant get_master_url'
        ))

        master_image.delete()

    def test_model_methods(self):
        master_image = create_image()
        master_image.__unicode__()

        # FIXME force reopen the file
        # why should I do that ?
        master_image.master.open()

        master_image.get_rendition_url(40, 40)
        # try to make this rendition again
        master_image.make_rendition(40, 40)

        # change master
        master_image.master = ContentFile(make_image().read(), 'toto.png')
        master_image.save()
        self.assertEqual(0, len(master_image.renditions))

        # change master with no alt name
        master_image.alternate_text = ''
        master_image.__unicode__()

        master_image.delete()

    def test_template_tags(self):
        master_image = create_image()

        # FIXME force reopen the file
        # why should I do that ?
        master_image.master.open()

        self.assertIsNotNone('<img', rendition(master_image, 12, 15))
        self.assertIsNotNone(rendition_url(master_image, 12, 15))
