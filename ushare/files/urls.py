from django.conf.urls import patterns, include, url

from .views import create_view, FileDetailView



urlpatterns = patterns('',
    url(r'^upload/$', create_view, name='upload'),
    url(r'^(?P<encoded_id>[-_\w]+)/$', FileDetailView.as_view(), name='detail'),
)
