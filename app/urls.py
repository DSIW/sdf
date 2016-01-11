# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # root
    url(r'^$', views.start_page_view, name='startPage'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # static
    url(r'^page/([a-z]+)$', views.staticPageView, name='staticpage'),

    # for testing
    url(r'^raise$', views.raise_exception),
]

