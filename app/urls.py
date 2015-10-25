from django.conf.urls import url

from . import views

urlpatterns = [
    # GET /
    url(r'^$', views.StartPageView.as_view(), name='startPage'),
    url(r'^archive/', views.archivesPageView, name='archivesPage'),
    url(r'^books/(?P<book_id>[0-9]+)/edit', views.archivesEditPageView, name='archivesEditPage'),
]
