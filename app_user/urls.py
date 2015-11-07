# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # accounts
    url(r'^accounts/register/$', views.register_user, name='register'),
    url(r'^accounts/emailconfirm/(?P<uuid>[0-9a-zA-Z]+)/$', views.confirm_email, name='confirm_email'),
    url(r'^accounts/(?P<pk>[0-9]+)/edit/$', views.UserUpdate.as_view(), name='edit_profile'),
]
