from django import template

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

register = template.Library()


@register.simple_tag
def active(request, pattern):
    """
    Returns 'active' if the give pattern is in the current URL.
    """
    try:
        if (request.path == '/' == pattern) or (pattern != '/' and request.path.startswith(pattern)):
            return 'active'
    except:  # pragma: no cover
        pass
    return ''
