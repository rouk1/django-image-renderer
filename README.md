# Django image renderer

[![Build Status](https://travis-ci.org/rouk1/django-image-renderer.svg?branch=master)](https://travis-ci.org/rouk1/django-image-renderer)
[![codecov.io](https://codecov.io/github/rouk1/django-image-renderer/coverage.svg?branch=master)](https://codecov.io/github/rouk1/django-image-renderer?branch=master)

Django image renderer is Django app that will help you render images in many sizes (renditions).

---

## Features

- uses [Pillow](https://github.com/python-pillow/Pillow) to resize images
- uses Django's _default_storage_ to let you play with whatever storage backend you'll need
- uploaded image files named using uuid
- rendition cached on disk


## Quick start

1. Add "renderer" to your INSTALLED_APPS setting like this::

```python
INSTALLED_APPS = (
    # your apps
    'renderer',
)
```

2. Include the polls URLconf in your project urls.py like this::

```python
url(r'^renderer/', include('renderer.urls')),
```

3. Run `python manage.py migrate` to create the renderer models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a MasterImage (you'll need the Admin app enabled).


## Sample project

TODO