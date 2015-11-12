#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from StringIO import StringIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from models import MasterImage


class RendererTest(TestCase):
    def create_superuser(self):
        username = 'admin'
        password = '123456'

        User.objects.create_superuser(username, 'a@a.fr', password)
        return username, password

    def create_image(self):
        image_file = StringIO()
        image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image.save(image_file, 'png')
        image_file.seek(0)
        master_image = MasterImage(
            master=ContentFile(image_file.read(), 'test-image.png'),
            alternate_text='test'
        )
        master_image.save()

        return master_image

    def test_create(self):
        master_image = self.create_image()
        self.assertTrue(MasterImage.objects.all() > 0)
        self.assertTrue(len(master_image.get_master_url()) > 0)
        self.assertTrue('test' not in master_image.get_master_filename())

    def test_rendition(self):
        master_image = self.create_image()
        # FIXME force reopen the file
        # why should I do that ?
        master_image.master.open()
        master_image.get_rendition_url(40, 40)

    def test_admin_pages(self):
        username, password = self.create_superuser()

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

        master_image = self.create_image()
        r = c.get(reverse('admin:renderer_masterimage_change', args=(master_image.pk, )))
        self.assertEqual(r.status_code, 200, (
            'cant access change page'
        ))