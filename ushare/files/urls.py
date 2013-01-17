from django.conf.urls import patterns, include, url
from django.conf import settings

from .views import create_view, FileDetailView, FileOEmbedView



urlpatterns = patterns('',
    url(r'^upload/$', create_view, name='upload'),
    url(r'^(?P<encoded_id>[%s]+)/$' % settings.SHORT_URL_ALPHABET, FileDetailView.as_view(), name='detail'),
    url(r'^(?P<encoded_id>[%s]+)/oembed/$' % settings.SHORT_URL_ALPHABET, FileOEmbedView.as_view(), name='oembed'),
)
