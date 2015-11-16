# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # root
    url(r'^$', views.StartPageView.as_view(), name='startPage'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # session
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, name='url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
