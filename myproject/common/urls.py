from django.conf import settings as config
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView

from myproject.common.admin import admin_site
from myproject.common.sitemaps import StaticViewSitemap
from myproject.common.views import home

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.1"

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    # Top-level URLs
    url(r'^admin/', admin_site.urls),

    # Crawler shortcuts and placeholders
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain; charset=utf-8')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=config.STATIC_URL + 'favicon.ico', permanent=True)),
    url(r'^favicon\.png$', RedirectView.as_view(url=config.STATIC_URL + 'favicon.png', permanent=True)),

    # General URLs
    url(r'^$', home, name='home'),
]
