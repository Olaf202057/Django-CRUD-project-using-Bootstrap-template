"""
Base URL configuration.
"""

import sys

from django.conf import settings as config
from django.conf.urls import include, url
from django.views import static

import myproject.auth.urls
import myproject.common.urls
import myproject.myapp.urls

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

urlpatterns = [
    # Include app-specific URL files
    url(r'^', include(myproject.common.urls)),
    url(r'^', include(myproject.auth.urls)),
    url(r'^', include(myproject.myapp.urls)),
]

if config.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if config.DEBUG or 'test' in sys.argv:
    # Ensure media files are shown properly when using a dev server
    urlpatterns += [
        url(r'^' + config.MEDIA_URL.lstrip('/') + '(?P<path>.*)$', static.serve, {
            'document_root': config.MEDIA_ROOT})
    ]
