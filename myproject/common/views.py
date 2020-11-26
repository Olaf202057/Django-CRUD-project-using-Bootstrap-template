"""
Unauthenticated general view entrance functions.
"""

import logging

from django.http import HttpResponseRedirect
from django.urls import reverse

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


def home(request):
    redirect = reverse('login')
    if request.user.is_authenticated():
        redirect = reverse('portal')

    return HttpResponseRedirect(redirect)
