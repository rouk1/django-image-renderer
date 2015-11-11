#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-image-renderer',
    version='0.1',
    packages=['renderer'],
    include_package_data=True,
    license='WTFPL',
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='https://github.com/rouk1/django-image-renderer',
    author='Matthieu Jouis',
    author_email='matthieu.jouis@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: WTFPL',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Pillow',
    ],
)
