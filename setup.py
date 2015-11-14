#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys


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
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    read_md = lambda f: open(f, 'r').read()

README = read_md('README.md')


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
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print "You probably want to also tag the version now:"
    print "  git tag -a %(version)s -m 'version %(version)s'" % args
    print "  git push --tags"
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
    install_requires=install_requires
)
