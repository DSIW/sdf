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

    # books
    url(r'^archive/',                               views.archivesPageView,     name='archivesPage'),
    url(r'^books/(?P<book_id>[0-9]+)/edit',         views.archivesEditPageView, name='archivesEditPage'),
    url(r'^books/(?P<id>[0-9]+)/delete$',           views.deleteBook,           name='deleteBook'),
    url(r'^accounts/(?P<user_id>[0-9]+)/showcase$', views.showcaseView,         name='user-showcase'),
    url(r'^books/(?P<id>[0-9]+)/publish$',          views.publishBook,          name='publishBook'),
    url(r'^books/(?P<id>[0-9]+)/unpublish$',        views.unpublishBook,        name='unpublishBook'),

    # accounts
    url(r'^accounts/register/$', views.register_user, name='register'),

    # search
    url(r'^search/$', views.searchBook, name='searchBook'),
    url(r'^search/results', views.searchBookResults, name='searchBookResults'),
]
