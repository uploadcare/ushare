from django.conf.urls import patterns, include, url

from .views import ImageFileCreateView, ImageFileDetailView



urlpatterns = patterns('',
    url(r'^upload/$', ImageFileCreateView.as_view(), name='upload'),
    url(r'^detail/(?P<pk>\d+)/$', ImageFileDetailView.as_view(), name='detail'),
)
