import markdown2
import codecs
import os

from random import randint
from django.conf import settings
from django.shortcuts import render
from renderer.models import MasterImage


def index(request):
    m = MasterImage.objects.first()
    readme_path = os.path.join(settings.BASE_DIR, '..', 'README.md')
    input_file = codecs.open(readme_path, mode='r', encoding='utf-8')
    text = input_file.read()
    text = text.split('## Sample project', 1)[0]
    html = markdown2.markdown(text, extras=['fenced-code-blocks', ])
    return render(request, 'demo/index.html', {
        'text': html,
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
