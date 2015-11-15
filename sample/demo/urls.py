from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ratio$', views.aspect_ration_renditions, name='ratio'),
    url(r'^random$', views.random_renditions, name='random'),
    url(r'^filters$', views.filters, name='filters'),
]
