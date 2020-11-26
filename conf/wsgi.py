"""
WSGI configuration for Django environment.
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

application = get_wsgi_application()

# Only start the monitor if we're using a non-dev web server and not in production
if not settings.DEV_SERVER:
    from conf import monitor

    monitor.start()
