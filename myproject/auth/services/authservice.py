"""
Authentication service functions.
"""

import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse

from myproject.common.utils import emailutils
from myproject.common.utils.viewutils import set_request_status

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


def process_register(request, user):
    """
    Complete the registration process and send the new user an email.

    :param request: the request being processed
    :param user: the user that has been created
    :return: a redirect to the next page in the registration flow
    """
    logger.info('Registered new user with username: {}'.format(user.get_username()))

    emailutils.send_multipart_email('email/register',
                                    {
                                        'PROJECT_NAME': settings.PROJECT_NAME,
                                        'site_url': settings.PROJECT_HOST,
                                        'login_url': reverse('login'),
                                    },
                                    'Welcome to {}'.format(settings.PROJECT_NAME), [user.email],
                                    [settings.DEFAULT_FROM_EMAIL])

    set_request_status(request, 'info', 'You\'re good to go. Login to get started!')

    return reverse('login')


def process_login(request, username, password):
    """
    Authenticate the user and log them if, if successful.

    :param request: the request being processed
    :param username: the username to authenticate
    :param password: the password to authenticate
    :return: a redirect to the next page in the login flow
    """
    redirect = None

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

        logger.info('Logged in user {}'.format(username))

        if request.POST.get('remember-me', False):
            request.session.set_expiry(1209600)

        # If 'next' exists as a parameter in the URL, redirect to the specified page instead
        if 'next' in request.GET:
            redirect = request.GET['next']
        else:
            redirect = reverse('portal')
    else:
        logger.info('Non-existent user {} attempted login'.format(username))

        set_request_status(request, 'warning',
                           'Oops! We don\'t recognize that account. Check to make sure you entered your '
                           'credentials properly.')

    return redirect


def process_logout(request):
    """
    Logout the currently authenticated user.

    :param request: the request being processed
    """
    email = request.user.email
    logout(request)
    logger.info('Logged out user {}'.format(email))


def process_forgot_password(request):
    """
    Generate a new password and send an email to the email specified in the request. For security purposes, whether
    the email exists in the system or not, the same response "success" will be shown the user.

    :param request: the request being processed
    :return: a redirect to the next page in the forgot password flow
    """
    email = request.POST['email']
    try:
        user = get_user_model().objects.get(email=email)

        # Generate a random password for the user
        password = get_user_model().objects.make_random_password()
        user.set_password(password)
        user.save()

        logger.info('Reset password for user with email {}'.format(email))

        emailutils.send_multipart_email('email/forgot',
                                        {
                                            'password': password,
                                            'site_url': settings.PROJECT_HOST,
                                            'settings_url': reverse('settings')
                                        },
                                        'Your Password Has Been Reset', [email])

        request.session.modified = True
    except get_user_model().DoesNotExist:
        logger.info('A visitor tried to reset the password for an unknown email address of {}'.format(email))

    set_request_status(request, 'info',
                       'You\'ve been emailed a temporary password. Login to your account immediately using the '
                       'temporary password, then change your password.')

    return reverse('login')
