from django.conf.urls import url

from . import views

urlpatterns = [
    # GET /
    url(r'^$', views.StartPageView.as_view(), name='startPage'),
    url(r'^archives/$', views.archivesPageView, name='archivesPage'),
]
