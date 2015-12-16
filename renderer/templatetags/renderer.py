#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import template
from django.utils.safestring import mark_safe

__author__ = 'rouk1'

register = template.Library()


@register.simple_tag
def rendition(master_image, width=0, height=0):
    w, h = master_image.get_rendition_size(width, height)
    node = '<img src="%s" width="%d" height="%d" alt="%s">' % (
        master_image.get_rendition_url(width, height),
        w,
        h,
        master_image.alternate_text
    )

    return mark_safe(node)


@register.simple_tag
def rendition_url(master_image, width=0, height=0):
    return master_image.get_rendition_url(width, height)