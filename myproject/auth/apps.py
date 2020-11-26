from django.apps import AppConfig

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class AuthConfig(AppConfig):
    name = 'myproject.auth'
    label = 'myproject_auth'
    verbose_name = 'Authentication'
