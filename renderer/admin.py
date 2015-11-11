#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models
from renderer.widgets import AdminImageWidget


class MasterImageAdmin(admin.ModelAdmin):
    list_display = (
        'admin_thumbnail',
        'alternate_text',
        'get_renditions_count',
        'pub_date',
        'last_modified'
    )
    list_display_links = (
        'admin_thumbnail',
        'alternate_text',
        'get_renditions_count',
        'pub_date',
        'last_modified'
    )
    search_fields = ('alternate_text', )
    list_filter = ('pub_date', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.ImageField):
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(MasterImageAdmin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)
