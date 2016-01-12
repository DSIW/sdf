# -*- coding: utf-8 -*-

from sdf.base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_CONTEXT_PROCESSORS = (
    'sdf.context_processors.debug',
)
ALLOWED_HOSTS = ['127.0.0.1','localhost']

ENDPOINT = "https://sdf.ngrok.com"

# Import local settings
try:
    from sdf.local_settings import *
except ImportError:
    import sys
    sys.stderr.write('Attention: sdf/local_settings.py not set. Use default local settings...\n')
    PAYPAL_RECEIVER_EMAIL = "test-facilitator@example.com"
    SEED_MAX_PAYPAL = "test-facilitator@example.com"
    SEED_MARTIN_PAYPAL = "test-buyer@example.com"
