from future.standard_library import install_aliases

install_aliases()

from urllib.parse import unquote

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


def set_request_status(request, status_type, message):
    """
    Set a 'status' of {'type', 'msg'} on the given request.

    :param request: the request being processed.
    :param status_type: the type of status to be displayed (match to Bootstrap alert types)
    :param message: the status message to be display
    """
    request.session['status'] = {'type': status_type, 'msg': message}


def get_request_status(request, default=None):
    """
    Return the 'status' attribute on the current request, if it exists. If successful, remove it from the request so the
    status is not processed again.

    :param request: the request being processed
    :param default: the default status, if one is not found on the request
    :return:
    """
    status = request.session.get('status', default)

    if not status:
        status_type = request.COOKIES.get('status_type', None)
        status_msg = request.COOKIES.get('status_msg', None)
        if status_type and status_msg:
            status = {'type': status_type, 'msg': unquote(status_msg)}

    if 'status' in request.session:
        del request.session['status']

    return status


def set_response_status(response, status):
    """
    Set the 'status_type' and 'status_msg' attributes on the given response's cookies.

    :param response: the response being processed
    :param status: the dict containing a status 'type' and 'msg'
    """
    if status:
        response.set_cookie('status_type', status['type'])
        response.set_cookie('status_msg', status['msg'])


def clear_response_status(response):
    """
    Clear the 'status_type" and 'status_msg' attributes of the given response's cookies.

    :param response: the response being processed
    """
    response.delete_cookie(key='status_type')
    response.delete_cookie(key='status_msg')
