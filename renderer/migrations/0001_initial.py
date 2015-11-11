# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import renderer.models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('master_width', models.PositiveIntegerField(null=True, editable=False)),
                ('master_height', models.PositiveIntegerField(null=True, editable=False)),
                ('master', models.ImageField(height_field=b'master_height', width_field=b'master_width', upload_to=renderer.models.get_unique_file_name)),
                ('alternate_text', models.CharField(max_length=256, blank=True)),
                ('renditions', picklefield.fields.PickledObjectField(editable=False, blank=True)),
            ],
        ),
    ]