from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^offers/(?P<id>[0-9]+)/start_payment/$', views.start_paypal_payment, name='start_paypal_payment'),
    url(r'^payments/(?P<id>[0-9]+)/redirection/$', views.paypal_redirection, name='paypal_redirection'),
    url(r'^payments/(?P<id>[0-9]+)/success/(?P<secret>[0-9a-zA-Z-]+)/$', views.paypal_complete, name='payment-success'),
    url(r'^payments/(?P<id>[0-9]+)/cancel/$', views.paypal_abort, name='payment-cancel'),
    url(r'^payments/(?P<id>[0-9]+)/rate/$', views.rate_seller, name='rate-seller'),
    url(r'^paypal/ipn-api/', include('paypal.standard.ipn.urls')),
]
