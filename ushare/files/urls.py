from django.conf.urls import patterns, include, url

from .views import create_view, ImageFileDetailView



urlpatterns = patterns('',
    url(r'^upload/$', create_view, name='upload'),
    url(r'^detail/(?P<pk>\d+)/$', ImageFileDetailView.as_view(), name='detail'),
)
