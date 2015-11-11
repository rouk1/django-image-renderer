# Django image renderer

Django image renderer is Django app that will help you render images in many sizes (renditions).

## Features

- uses [Pillow](https://github.com/python-pillow/Pillow) to resize images
- uses Django's _default_storage_ to let you play with whatever storage backend you'll need
- generates image name using uuid

## Quick start

1. Add "renderer" to your INSTALLED_APPS setting like this::

```
    INSTALLED_APPS = (
        ...
        'polls',
    )
```

2. Include the polls URLconf in your project urls.py like this::

```
    rl(r'^renderer/', include('renderer.urls')),
```

3. Run `python manage.py migrate` to create the renderer models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a MasterImage (you'll need the Admin app enabled).
