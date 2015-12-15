# -*- coding: utf-8 -*-

"""
Django settings for sdf project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib.messages import constants as message_constants
DEFAULT_CHARSET='utf-8'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'fixtures'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'watson',
    'paypal.standard.ipn',
    'django_extensions',
    'app',
    'braces',
    'app_book',
    'app_user',
    'app_payment',
    'app_notification',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'app.middleware.http_method_middleware.HttpMethodMiddleware', # before CsrfViewMiddleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'app.middleware.current_user_middleware.CurrentUserMiddleware', # after SessionAuthenticationMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sdf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                'app_notification.context_processors.unread_notification_exist',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file-debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log'
        },
        'file-error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/error.log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file-debug'],
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file-error'],
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'propagate': False,
        }
    }
}

WSGI_APPLICATION = 'sdf.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.gmx.net'
EMAIL_PORT = '587'
EMAIL_HOST_PASSWORD = 'htwberlin'
EMAIL_HOST_USER = 'sdf-phb@gmx.de'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

ADMINS = [('Max', 'studium@mluz.de'), ('Jens', 'ottmann.jens@googlemail.com')]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# NOTE: Trailing slash is important!
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files (book-images, profil-images)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Secret Key Generator
if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(BASE_DIR, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = open(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

#Paypal
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "ottmann.jens@googlemail.com"
ENDPOINT = "https://ws15sdf-b.f4.htw-berlin.de/paypal/ipn-api/"

UNPAID_PAYMENT_TIMEOUT = 30*60 # 30 minutes
