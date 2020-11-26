"""
Authentication view entrance functions.
"""

import logging

import pytz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from myproject.auth.forms.userloginform import UserLoginForm
from myproject.auth.forms.userregistrationform import UserRegisterForm
from myproject.auth.services import authservice
from myproject.common.utils.viewutils import set_response_status, get_request_status, set_request_status, \
    clear_response_status

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


def register(request):
    redirect = None

    if request.user.is_authenticated():
        redirect = reverse('portal')

    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            user_register_form.save()

            redirect = authservice.process_register(request, user_register_form.instance)
        else:
            set_request_status(request, 'warning', list(user_register_form.errors.values())[0][0])
    else:
        user_register_form = UserRegisterForm()

    # Check if a status has been set (either by this view or another view from which we were redirect)
    status = get_request_status(request, '')

    if redirect:
        response = HttpResponseRedirect(redirect)

        # In the case of a redirect, we move the status to the response so it gets passed
        set_response_status(response, status)

        return response
    else:
        data = {
            'form': user_register_form,
            'status': status
        }

        return render(request, 'authentication/register.html', data)


def login(request):
    redirect = None
    status = None

    user_login_form = UserLoginForm()
    if request.user.is_authenticated():
        redirect = reverse('portal')
    else:
        if request.method == 'POST':
            user_login_form = UserLoginForm(request.POST)
            if user_login_form.is_valid():
                username = user_login_form.cleaned_data.get('username')
                password = user_login_form.cleaned_data.get('password')

                redirect = authservice.process_login(request, username, password)
            else:
                set_request_status(request, 'warning', list(user_login_form.errors.values())[0][0])

        status = get_request_status(request, None)

    # Login was successful, or the user is already logged in
    if redirect:
        redirect = HttpResponseRedirect(redirect)

        return redirect
    else:
        http_status = 200
        if request.method == 'POST':
            http_status = 401

        data = {
            'form': user_login_form,
            'status': status
        }

        response = render(request, 'authentication/login.html', data, status=http_status)
        clear_response_status(response)
        return response


def logout(request):
    if request.user.is_authenticated():
        authservice.process_logout(request)

    return HttpResponseRedirect(reverse('portal'))


def forgot(request):
    redirect = None
    status = None

    if request.user.is_authenticated():
        redirect = reverse('settings')
    else:
        if request.method == 'POST':
            redirect = authservice.process_forgot_password(request)

        status = get_request_status(request)

    if not redirect:
        data = {
            'status': status
        }

        return render(request, 'authentication/forgot.html', data)
    else:
        response = HttpResponseRedirect(redirect)

        set_response_status(response, status)

        return response


@login_required
def settings(request):
    timezone.activate(pytz.timezone(request.user.time_zone))

    return render(request, "settings.html")
