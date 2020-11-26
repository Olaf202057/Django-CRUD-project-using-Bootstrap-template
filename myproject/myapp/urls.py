"""
Authenticated app URLs.
"""

from django.conf.urls import url

from myproject.myapp.views import portal

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

urlpatterns = [
    # Authenticated URLs
    url(r'^portal', portal, name='portal'),
]
