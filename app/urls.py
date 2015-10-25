from django.conf.urls import url

from . import views

urlpatterns = [
    # GET /
    url(r'^$', views.StartPageView.as_view(), name='startPage'),
    url(r'^archives/archives.html', views.archivesPageView, name='archivesPage'),
    url(r'^archives/(?P<book_id>[0-9]+)/archivesedit.html', views.archivesEditPageView, name='archivesEditPage'),
]
