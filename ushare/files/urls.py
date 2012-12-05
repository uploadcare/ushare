from django.conf.urls import patterns, include, url

from .views import create_view, ImageFileDetailView



urlpatterns = patterns('',
    url(r'^upload/$', create_view, name='upload'),
    url(r'^(?P<slug>[-_\w]+)/(?P<filename>[-_.%\w]+)?$', ImageFileDetailView.as_view(), name='detail'),
)
