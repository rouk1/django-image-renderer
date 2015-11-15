#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from renderer.models import MasterImage
from renderer.widgets import AdminImageWidget


@admin.register(MasterImage)
class MasterImageAdmin(admin.ModelAdmin):
    list_display = (
        'get_thumbnail',
        'alternate_text',
        'get_renditions_count',
        'pub_date',
        'last_modified'
    )
    list_display_links = (
        'get_thumbnail',
        'alternate_text',
        'get_renditions_count',
        'pub_date',
        'last_modified'
    )
    search_fields = ('alternate_text',)
    list_filter = ('pub_date',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.ImageField):
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(MasterImageAdmin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)

    def get_renditions_count(self, obj):
        return '%d rendition(s)' % len(obj.renditions)

    get_renditions_count.short_description = _('number of renditions')

    def get_thumbnail(self, obj):
        '''admin image tag for easy browse'''
        t = (obj.get_rendition_url(100), obj.alternate_text)
        return '<img src="%s" alt="%s"/>' % t

    get_thumbnail.allow_tags = True
    get_thumbnail.short_description = _('thumbnail')
