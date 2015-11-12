#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from StringIO import StringIO

import os
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase
from models import MasterImage


class RendererTest(TestCase):
    def create_image(self):
        image_file = StringIO()
        image = Image.new('RGBA', size=(50,50), color=(256,0,0))
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
