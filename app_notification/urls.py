# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^notifications/', views.notificationPageView, name='notificationsPage'),
    url(r'^notificationSendBook/(?P<id>[0-9]+)', views.notificationSendBookPageView, name='notificationsSendBookPage'),
]
