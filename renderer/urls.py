#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^rendition/url/(?P<image_id>\d+)/(?P<target_width>\d+)/(?P<target_height>\d+)/$',
        views.get_rendition_url,
        name='get_rendition_url'
    ),
    url(
        r'^master/url/(?P<image_id>\d+)/$',
        views.get_master_url,
        name='get_master_url'
    ),
]
