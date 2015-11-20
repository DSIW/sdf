# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
from django.conf.urls import include, url

urlpatterns = [
    # accounts
    url(r'^accounts/register/$', views.register_user, name='register'),
    url(r'^accounts/emailconfirm/(?P<uuid>[0-9a-zA-Z]+)/$', views.confirm_email, name='confirm_email'),
    url(r'^accounts/(?P<pk>[0-9]+)/edit/$', views.UserUpdate.as_view(), name='edit_profile'),
    url(r'^accounts/password/(?P<uuid>[0-9a-zA-Z]+)/$',views.password_new, name='new_password'),
    url(r'^accounts/password/', views.changePassword, name='change_password'),
    url(r'^password_reset/$',views.password_reset, name='reset_password'),
    url(r'^login/$', views.login_user, name='login'),
]
