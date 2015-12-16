#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys
import shutil


name = 'django-image-renderer'
package = 'renderer'
description = 'render image in various sizes'
url = 'https://github.com/rouk1/django-image-renderer'
author = 'rouk1'
author_email = 'matthieu.jouis@gmail.com'
license = 'WTFPL'
install_requires = [
    'Pillow>=3.0.0',
    'django-picklefield>=0.3.2'
]

try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = ''


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]",
        init_py,
        re.MULTILINE
    ).group(1)


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep pypandoc"):
        print("pypandoc not installed.\nInstall pandoc then Use `pip install pypandoc`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    v = get_version(package)
    print("  git tag -a %s -m 'version %s'" % (v, v))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_image_renderer.egg-info')
    sys.exit()


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    long_description=README,
    author=author,
    author_email=author_email,
    packages=[package],
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
