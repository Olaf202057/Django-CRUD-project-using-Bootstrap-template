#!/usr/bin/env python
"""
Management script for Django environment.
"""

import os
import sys

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
