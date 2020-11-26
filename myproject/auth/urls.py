"""
Authentication URLs.
"""

from django.conf.urls import url

from myproject.auth.views import login, logout, forgot, settings, register

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

urlpatterns = [
    # Authentication URLs
    url(r'^register$', register, name='register'),
    url(r'^login$', login, name='login'),
    url(r'^logout', logout, name='logout'),
    url(r'^forgot$', forgot, name='forgot'),

    # Account URLs
    url(r'^settings$', settings, name='settings'),
]
