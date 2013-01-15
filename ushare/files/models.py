from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from pyuploadcare.dj import FileField

from .utils import get_extension, encode_url
from .validators import extension_validator, size_validator



class BaseAbstractFile(models.Model):
    file_obj = FileField(verbose_name=_(u'file'), null=True, validators=[extension_validator, size_validator,])
    file_id = models.TextField(_(u'uploadcare id'), default=u'', editable=False)
    date_created = models.DateTimeField(_(u'date created'), auto_now_add=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        self.file_id = self.file_obj.info[u'file_id']
        return super(BaseAbstractFile, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('files:detail', (self.encoded_id,))

    def url(self, use_https=False):
        mapping = {
            'protocol': 'https' if use_https else 'http',
            'domain': Site.objects.get_current(),
            'url': self.get_absolute_url(),
        }
        return u'%(protocol)s://%(domain)s%(url)s' % mapping

    @property
    def encoded_id(self):
        return encode_url(self.id)

    # A bunch of proxy-methods.

    @property
    def filename(self):
        return self.file_obj.info[u'original_filename'].strip('/')

    @property
    def extension(self):
        return get_extension(self.filename)

    @property
    def is_image(self):
        return self.file_obj.info[u'is_image']

    @property
    def size(self):
        return self.file_obj.info[u'size']

    @property
    def mime_type(self):
        return self.file_obj.info[u'mime_type']


class File(BaseAbstractFile):

    class Meta:
        verbose_name = _(u'file')
        verbose_name_plural = _(u'files')

    def __unicode__(self):
        return u'%s' % self.file_obj.cdn_url
