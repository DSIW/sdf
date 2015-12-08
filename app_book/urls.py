# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # books
    url(r'^accounts/(?P<user_id>[0-9]+)/showcase$', views.showcaseView, name='showcase'),
    url(r'^archive/', views.archivesPageView, name='archivesPage'),
    url(r'^books/create', views.createBook, name='createBook'),
    url(r'^books/(?P<id>[0-9]+)/edit', views.editBook, name='editBook'),
    url(r'^books/(?P<id>[0-9]+)/delete$', views.deleteBook, name='deleteBook'),
    url(r'^books/(?P<id>[0-9]+)/publish$', views.publishBook, name='publishBook'),
    url(r'^books/(?P<id>[0-9]+)/unpublish$', views.unpublishBook, name='unpublishBook'),
    url(r'^books/(?P<id>[0-9]+)/', views.detailView, name='book-detail'),

    # search
    url(r'^search/results', views.searchBookResults, name='searchBookResults'),

    # offers
    url(r'^offers/(?P<id>[0-9]+)/new_counteroffer', views.counteroffer, name='new_counteroffer'),
    url(r'^counteroffers/(?P<id>[0-9]+)/accept', views.accept_counteroffer, name='accept_counteroffer'),
    url(r'^counteroffers/(?P<id>[0-9]+)/decline', views.decline_counteroffer, name='decline_counteroffer'),
]

