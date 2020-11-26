"""
Settings specific to prod-like deployable code, reading values from system environment variables.
"""

import os

from conf.configs import common
from conf.settings import PROJECT_ID

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.0"

# Application definition

INSTALLED_APPS = common.INSTALLED_APPS

MIDDLEWARE = common.MIDDLEWARE

TEMPLATES = common.TEMPLATES

if common.DEBUG:
    TEMPLATES[0]['OPTIONS']['context_processors'] += (
        'django.template.context_processors.debug',
    )

#############################
# Django configuration
#############################

# Security

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Logging

if not common.DEBUG:
    ADMINS = (
        (common.PROJECT_NAME, common.ADMIN_EMAIL_ADDRESS),
    )
    MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'django': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/django.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'myproject_common': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/common.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'myproject_auth': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/auth.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'myproject_myapp': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/myapp.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.common': {
            'handlers': ['myproject_common', 'mail_admins'],
            'level': 'INFO',
        },
        'myproject.auth': {
            'handlers': ['myproject_auth', 'mail_admins'],
            'level': 'INFO',
        },
        'myproject.myapp': {
            'handlers': ['myproject_myapp', 'mail_admins'],
            'level': 'INFO',
        },
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('MYPROJECT_REDIS_HOST'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

# Database

DATABASES = {
    'default': {
        'NAME': os.environ.get('MYPROJECT_DB_NAME'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('MYPROJECT_DB_HOST'),
        'USER': os.environ.get('MYPROJECT_DB_USER'),
        'PASSWORD': os.environ.get('MYPROJECT_DB_PASSWORD'),
    }
}
