from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from pyuploadcare.dj import FileField



class BaseAbstractFile(models.Model):
    file = FileField(verbose_name=_(u'file'), null=True)
    file_id = models.TextField(_(u'uploadcare id'), default=u'', blank=True)
    date_created = models.DateTimeField(_(u'date created'), auto_now_add=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

    @models.permalink
    def get_absolute_url(self):
        return ('files:detail', (self.file_id,))

    def url(self, use_https=False):
        mapping = {
            'protocol': 'https' if use_https else 'http',
            'domain': Site.objects.get_current(),
            'url': self.get_absolute_url(),
        }
        return u'%(protocol)s://%(domain)s%(url)s' % mapping


class ImageFile(BaseAbstractFile):

    class Meta:
        verbose_name = _(u'image file')
        verbose_name_plural = _(u'image files')

    def __unicode__(self):
        return u'%s' % self.file.cdn_url
