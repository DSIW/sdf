from django.contrib import admin
from paypal.standard.ipn.models import PayPalIPN

admin.site.unregister(PayPalIPN)