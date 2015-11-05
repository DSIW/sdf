# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # root
    url(r'^$', views.StartPageView.as_view(), name='startPage'),

    # session
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, name='url'),
]
