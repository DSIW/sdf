# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # root
    url(r'^$', views.StartPageView.as_view(), name='startPage'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # session

    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^imprint$', views.page_info, {"template_name":"app/page_info.html","title":"Impressum"}, name='imprint'),
    url(r'^agb$', views.page_info, {"template_name":"app/page_info.html","title":"AGB"}, name='agb'),
    url(r'^privacy$', views.page_info, {"template_name":"app/page_info.html","title":"Datenschutz"}, name='privacy'),
    url(r'^affiliate$', views.page_info, {"template_name":"app/page_info.html","title":"Affiliate"}, name='affiliate'),
    url(r'^team$', views.page_info, {"template_name":"app/page_info.html","title":"Team"}, name='team'),
    url(r'^job$', views.page_info, {"template_name":"app/page_info.html","title":"Job"}, name='job'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

