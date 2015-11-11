from django.shortcuts import render
from renderer.models import MasterImage
from random import randint

def index(request):
    m = MasterImage.objects.first()
    renditions = [(0, 0)]
    for i in range(0, 8):
        renditions.append((
            randint(0, m.master_width),
            randint(0, m.master_height),
        ))
    return render(request, 'demo/index.html', {
        'master': m,
        'renditions': renditions,
    })