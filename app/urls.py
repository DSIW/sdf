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

    url(r'^faq/$',views.faq_list, name='faq_list'),
    url(r'^faq/(?P<id>[0-9]+)/$',views.faq,name='faq'),
    url(r'^faq/create/$',views.faq_create,name='faq_create'),
    url(r'^faq/(?P<id>[0-9]+)/delete/$',views.faq_delete,name='faq_delete'),
    url(r'^faq/(?P<id>[0-9]+)/edit/$',views.faq_edit,name='faq_edit'),



    url(r'^page/([a-z]+)$', views.staticPageView, name='staticpage'),

    # for testing
    url(r'^raise$', views.raise_exception),
]

