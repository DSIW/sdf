# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # books
    url(r'^archive/', views.archivesPageView, name='archivesPage'),
    url(r'^books/(?P<book_id>[0-9]+)/edit', views.archivesEditPageView, name='archivesEditPage'),
    url(r'^books/(?P<id>[0-9]+)/delete$', views.deleteBook, name='deleteBook'),

    # search
    url(r'^search/$', views.searchBook, name='searchBook'),
    url(r'^search/results', views.searchBookResults, name='searchBookResults'),
]
