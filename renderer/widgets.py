#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from renderer.models import MasterImage


class AdminImageWidget(forms.FileInput):
    '''
    A ImageField Widget for admin that shows a thumbnail.
    '''

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if (
            value and hasattr(value.instance, 'get_rendition_url') and
            hasattr(value, 'url')
        ):
            url = value.instance.get_rendition_url(100)
            output.append('<a target="_blank" href="%s">'
                          '<img src="%s" width="100" /></a> '
                          % (value.url, url))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(''.join(output))


class MasterImageWidget(ForeignKeyRawIdWidget):
    ''' a simple image widget'''

    class Media:
        js = ('renderer/admin/js/master-image-widget.js',)
        css = {
            'all': ('renderer/admin/css/master-image-widget.css',)
        }

    def render(self, name, value, attrs=None):
        attrs = attrs or {}

        attrs['class'] = 'vForeignKeyRawIdAdminField vForeignMasterImageWidget'
        url = reverse('renderer:get_rendition_url', args=[1, 1, 1])
        attrs['data-get-rendition-url'] = url.replace('1/1/1/', '')

        if value:
            master_url = MasterImage.objects.get(pk=value).get_master_url()
            attrs['data-get-master-url'] = master_url

        return super(MasterImageWidget, self).render(name, value, attrs=attrs)

    def label_for_value(self, value):
        return ''


class MasterImageAdminMixin(object):
    '''use this mixin to have a better widget in admin forms'''

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.rel.to == MasterImage:
            db = kwargs.get('using')
            kwargs['widget'] = MasterImageWidget(
                db_field.rel,
                self.admin_site,
                using=db
            )
        return super(MasterImageAdminMixin, self).formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )
