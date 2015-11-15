from random import randint

from django.shortcuts import render
from renderer.models import MasterImage


def index(request):
    m = MasterImage.objects.first()
    return render(request, 'demo/index.html', {
        'master': m,
    })


def aspect_ration_renditions(request):
    m = MasterImage.objects.first()
    renditions = []
    for i in range(0, 4):
        renditions.append((
            randint(0, min(m.master_width, 768/2)),
            0,
        ))
    for i in range(0, 4):
        renditions.append((
            0,
            randint(0, m.master_height),
        ))
    return render(request, 'demo/ratio.html', {
        'master': m,
        'renditions': renditions,
    })


def random_renditions(request):
    m = MasterImage.objects.first()
    renditions = []
    for i in range(0, 8):
        renditions.append((
            randint(0, min(m.master_width, 768/2)),
            randint(0, m.master_height),
        ))
    return render(request, 'demo/random.html', {
        'master': m,
        'renditions': renditions,
    })


def filters(request):
    m = MasterImage.objects.first()
    return render(request, 'demo/index.html', {
        'master': m,
        'renditions': [],
    })
