from django.conf.urls import url

from . import views

urlpatterns = [
    # GET /
    url(r'^$', views.StartPageView.as_view(), name='startPage'),
]
