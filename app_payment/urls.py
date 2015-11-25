from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^offers/(?P<id>[0-9]+)/start_payment$', views.start_paypal_payment, name='start_paypal_payment'),
    url(r'^paypal/success/$', views.paypal_complete, name='paypal-payment-success'),
    url(r'^paypal/cancel/$', views.paypal_abort, name='paypal-payment-cancel'),
    url(r'^paypal/ipn-api/', include('paypal.standard.ipn.urls')),
]
