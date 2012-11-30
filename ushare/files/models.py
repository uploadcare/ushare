from django.db import models
from django.utils.translation import ugettext_lazy as _

from pyuploadcare.dj import FileField



class BaseAbstractFile(models.Model):
    file = FileField(verbose_name=_(u'file'))
    date_created = models.DateTimeField(_(u'date created'), auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

    @models.permalink
    def get_absolute_url(self):
        return ('files:detail', (self.id,))


class ImageFile(BaseAbstractFile):

    class Meta:
        verbose_name = _(u'image file')
        verbose_name_plural = _(u'image files')

    def __unicode__(self):
        return u'%s' % self.file.cdn_url
