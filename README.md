# Django image renderer

[![Build Status](https://travis-ci.org/rouk1/django-image-renderer.svg?branch=master)](https://travis-ci.org/rouk1/django-image-renderer)
[![Coverage](https://codecov.io/github/rouk1/django-image-renderer/coverage.svg?branch=master)](https://codecov.io/github/rouk1/django-image-renderer?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/django-image-renderer.svg)](https://pypi.python.org/pypi/django-image-renderer)

Django image renderer is an app that will help you render images in many sizes (renditions).
This can be really helpful for generating images size for different screens resolution (especially when targeting mobile).

---

## Features

- uses [Pillow](https://github.com/python-pillow/Pillow) to resize images
- uses Django's _default_storage_ to let you play with whatever storage backend you'll need
- uploaded image files named using uuid
- rendition cached on disk
- resize keeping original aspect ratio
- crop if needed
- simple widget for admin site

## Quick start

Install the app.

```sh
pip install django-image-renderer
```

Add "renderer" to your INSTALLED_APPS setting like this:

_settings.py_

```python
INSTALLED_APPS = (
    # your apps
    'renderer',
)
```

Include the renderer URL configuration in your project _urls.py_ like this:

_urls.py_

```python
url(r'^renderer/', include('renderer.urls', namespace='renderer')),
```

Run `python manage.py migrate` to create the renderer models.

Start the development server and visit http://localhost:8000/admin/
to create a MasterImage (you'll need the Admin app enabled).

## Requirements

- Python (2.7, 3.4, 3.5)
- Django (1.7, 1.8, 1.9)

## Usage

There is only one model in the app: _MasterImage_.
With a _MasterImage_ you can ask for renditions.

```python
m = MasterImage.objects.first()

# get the master file's URL
m.get_master_url()
# or
m.get_rendition_url(0, 0)

# cache and return URL of a renditions that as 200 pixels width
# and height computed according to master's aspect ratio
url = m.get_rendition_url(200, 0)

# cache and return URL of a renditions that as 50 pixels height
# and width computed according to master's aspect ratio
url = m.get_rendition_url(0, 50)
```

If you ask for a size that do not fit master's aspect ration you'll receive a center cropped image.

You can also ask for a rendition in templates.

_models.py_

```python
def index(request):
    m = MasterImage.objects.first()
    return render(request, 'demo/index.html', {
        'master': m,
    })
```

_index.html_

```HTML+Django
{% load renderer %}
...
{% rendition master 42 42 %}
...
{% rendition_url 42 42 %}
...
```

This will render as:

```HTML
<img src="/media/img/0fb34de8-9d83-456a-828b-72ab21f8ebab_42x42.png" width="42" height="42" alt="">
...
/media/img/0fb34de8-9d83-456a-828b-72ab21f8ebab_42x42.png
...
```

When using _MasterImage_ in your model you may need a widget who provides a preview for you image.
For convenience a mixin is provided.

_models.py_

```python
from django.db import models

class DemoModel(models.Model):
    master = models.ForeignKey('renderer.MasterImage')
```

_admin.py_

```python
from demo.models import DemoModel
from django.contrib import admin
from renderer.widgets import MasterImageAdminMixin

@admin.register(DemoModel)
class DemoModelAdmin(MasterImageAdminMixin, admin.ModelAdmin):
    fields = ('master', )
```

## Sample project

A sample project is available in the [sample](https://github.com/rouk1/django-image-renderer/tree/master/sample) folder.
Test it as an usual Django project:

```sh
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python sample/manage.py migrate
python sample/manage.py createsuperuser
python sample/manage.py runserver
```

It' also deployed at http://django-image-renderer.herokuapp.com/.
