# -*- coding: utf-8 -*-

from sdf.base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_CONTEXT_PROCESSORS = (
    'sdf.context_processors.debug',
)
ALLOWED_HOSTS = []

# Import local settings
try:
    from sdf.local_settings import *
except ImportError:
    import sys
    sys.stderr.write('Attention: sdf/local_settings.py not set\n')
