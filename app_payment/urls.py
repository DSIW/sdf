from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^offers/(?P<id>[0-9]+)/start_payment$', views.start_paypal_payment, name='start_paypal_payment'),
    url(r'^payments/(?P<id>[0-9]+)/success/$', views.paypal_complete, name='payment-success'),
    url(r'^payments/(?P<id>[0-9]+)/cancel/$', views.paypal_abort, name='payment-cancel'),
    url(r'^paypal/ipn-api/', include('paypal.standard.ipn.urls')),
]
