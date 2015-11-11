from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import last_modified
from .models import MasterImage


def get_last_modified(request, image_id, target_width=0, target_height=0):
    im = get_object_or_404(MasterImage, pk=image_id)
    return im.last_modified


@last_modified(last_modified_func=get_last_modified)
def get_rendition_url(request, image_id, target_width=0, target_height=0):
    '''
    get a rendition url

    if the rendition does nto exist it will be created in the storage
    if dimensions do not fit master's aspect ratio
    then image will be cropped with a centered anchor

    if one dimensions is omitted (0)
    the other one will be generated accordind to master's aspect ratio

    :param request: http GET request
        /renderer/rendition/url/<image_id>/<target_width>/<target_height>/
    :param image_id: the master image primary key
    :param target_width: target image width
        if 0 renderer will use target_height
        to generate a image with correct aspect ratio
    :param target_height: target image height
        if 0 renderer will use target_width
        to generate a image height correct aspect ratio
    :return: rendition url in a json dictionary
    '''
    im = get_object_or_404(MasterImage, pk=image_id)

    return JsonResponse({
        'url': im.get_rendition_url(target_width, target_height)
    })


@last_modified(last_modified_func=get_last_modified)
def get_master_url(request, image_id):
    '''
    get image's master url

    ...

    :param request: http GET request /renderer/master/url/<image_id>/
    :param image_id: the master image primary key
    :return: master url in a json dictionary
    '''
    im = get_object_or_404(MasterImage, pk=image_id)

    return JsonResponse({'url': im.get_master_url()})
