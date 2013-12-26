from django.conf.urls import patterns, url
from django.conf import settings

from .views import create_view, FileDetailView


urlpatterns = patterns(
    '',
    url(r'^upload/$',
        view=create_view,
        name='upload'),
    url(r'^(?P<encoded_id>[{}]+)/(?P<filename>[\-\%%\w\W]+)?$'.format(settings.SHORT_URL_ALPHABET),
        view=FileDetailView.as_view(),
        name='detail'),
)
