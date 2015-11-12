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
- resize keeping orignal aspect ratio
- crop if needed
- simple MasterImage widget for admin site

## Quick start

Add "renderer" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = (
    # your apps
    'renderer',
)
```

Include the renderer URLconf in your project urls.py like this:

```python
url(r'^renderer/', include('renderer.urls', namespace='renderer'))),
```

Run `python manage.py migrate` to create the renderer models.

Start the development server and visit http://127.0.0.1:8000/admin/
to create a MasterImage (you'll need the Admin app enabled).

## Usage

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

## Sample project

A sample project is available in the [sample](https://github.com/rouk1/django-image-renderer/tree/master/sample) folder.
Test it as an usual django project:

```sh
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python sample/manage.py migrate
python sample/manage.py createsuperuser
python sample/manage.py runserver
```
