# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # books
    url(r'^accounts/(?P<user_id>[0-9]+)/showcase$', views.showcaseView, name='showcase'),
    url(r'^archive/', views.archivesPageView, name='archivesPage'),
    url(r'^books/(?P<id>[0-9]+)/edit', views.editBook, name='editBook'),
    url(r'^books/create', views.createBook, name='createBook'),
    url(r'^books/newest', views.newestBooks, name='newestBooks'),
    url(r'^books/(?P<id>[0-9]+)/delete$', views.deleteBook, name='deleteBook'),
    url(r'^books/(?P<id>[0-9]+)/publish$', views.publishBook, name='publishBook'),
    url(r'^books/(?P<id>[0-9]+)/unpublish$', views.unpublishBook, name='unpublishBook'),

    # search
    url(r'^search/results', views.searchBookResults, name='searchBookResults'),
]
