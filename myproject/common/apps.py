from future.moves import sys
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.4"


class CommonConfig(AppConfig):
    name = 'myproject.common'
    verbose_name = 'Common'

    def ready(self):
        if settings.DEV_SERVER and settings.USE_NGROK:
            # pyngrok will only be installed, and should only ever be initialized, in a dev environment
            from pyngrok import ngrok

            # Get the dev server port (defaults to 8000 for Django, can be overridden with the
            # last arg when calling `runserver`)
            addrport = urlparse("http://{}".format(sys.argv[-1]))
            port = addrport.port if addrport.netloc and addrport.port else 8000

            # Open a ngrok tunnel to the dev server
            public_url = ngrok.connect(port)
            print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

            # Update any base URLs or webhooks to use the public ngrok URL
            settings.PROJECT_HOST = public_url
            CommonConfig.init_webhooks(public_url)

    @staticmethod
    def init_webhooks(callback_url):
        pass
