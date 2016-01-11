# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
from django.conf.urls import include, url

urlpatterns = [
    # accounts
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/register/$', views.register_user, name='register'),
    url(r'^accounts/resend_confirmation_mail/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,20})/$$', views.resend_confirmation_mail, name='resend_confirmation_mail'),
    url(r'^accounts/emailconfirm/(?P<uuid>[0-9a-zA-Z]+)/$', views.confirm_email, name='confirm_email'),
    url(r'^accounts/(?P<pk>[0-9]+)/edit/$', views.user_update, name='edit_profile'),
    url(r'^accounts/(?P<pk>[0-9]+)/toggleStaff$', views.toggleStaff, name='user-toggle_staff'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.user_details, name='user-details'),
    url(r'^accounts/password/(?P<uuid>[0-9a-zA-Z]+)/$',views.password_new, name='new_password'),
    url(r'^accounts/password/', views.changePassword, name='change_password'),
    url(r'^accounts/(?P<id>[0-9]+)/ratings/$', views.user_ratings, name='user_ratings'),
    url(r'^accounts/(?P<change_user_data_id>[0-9]+)/change_user_profile_decline/$', views.change_user_profile_decline, name='change_user_profile_decline'),
    url(r'^accounts/(?P<change_user_data_id>[0-9]+)/change_user_profile_accept/$', views.change_user_profile_accept, name='change_user_profile_accept'),
    url(r'^password_reset/$', views.password_reset, name='reset_password'),
]
