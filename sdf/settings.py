# -*- coding: utf-8 -*-

from sdf.base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_CONTEXT_PROCESSORS = (
    'sdf.context_processors.debug',
)
ALLOWED_HOSTS = ['127.0.0.1','localhost']
