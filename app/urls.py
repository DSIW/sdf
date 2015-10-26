from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # root
    url(r'^$', views.StartPageView.as_view(), name='startPage'),

    # session
    url(r'^login$', auth_views.login, {}),
    url(r'^logout$', auth_views.logout, {'template_name': 'app/start.html'}),

    # books
    url(r'^archive/', views.archivesPageView, name='archivesPage'),
    url(r'^books/(?P<book_id>[0-9]+)/edit', views.archivesEditPageView, name='archivesEditPage'),
    url(r'^books/(?P<id>[0-9]+)/delete$', views.deleteBook, name='deleteBook'),
]
