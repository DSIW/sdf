# -*- coding: utf-8 -*-

from sdf.base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.htw-berlin.de', # Allow domain and subdomains
]

# Paypal
ENDPOINT = "https://ws15sdf-b.f4.htw-berlin.de:8080"
