#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from django.conf import settings
from django.core.files import File
from django.test import TestCase
from models import MasterImage


class RendererTest(TestCase):
    def create_test_file(self):
        test_file_path = os.path.join(
            settings.BASE_DIR,
            '..',
            'doc',
            'img',
            'bender.png'
        )
        with open(test_file_path) as test_file:
            master_image = MasterImage(
                master=File(test_file),
                alternate_text='bender'
            )
            master_image.save()

        return master_image

    def test_create(self):
        master_image = self.create_test_file()
        self.assertTrue(MasterImage.objects.all() > 0)
        self.assertTrue(len(master_image.get_master_url()) > 0)
        self.assertTrue('bender' not in master_image.get_master_filename())

    def test_rendition(self):
        master_image = self.create_test_file()
        master_image.get_rendition_url(40, 40)


