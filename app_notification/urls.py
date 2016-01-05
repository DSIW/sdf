# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^notifications/(?P<id>[0-9]+)/read/', views.read_notification, name='read-notification'),
    url(r'^notifications/toggleEmail/', views.notificationEmailToggle, name='notificationEmailToggle'),
    url(r'^notifications/', views.notificationPageView, name='notificationsPage'),
    url(r'^notificationSendBook/(?P<id>[0-9]+)', views.notificationSendBookPageView, name='notificationsSendBookPage'),
]
