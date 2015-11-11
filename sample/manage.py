#!/usr/bin/env python
import os
import sys

SAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    sys.path.append(os.path.join(SAMPLE_DIR, '..'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
