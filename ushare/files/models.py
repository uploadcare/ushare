from urllib import urlopen
from pygments import lexers, formatters, highlight, styles
from pygments.util import ClassNotFound

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings

from pyuploadcare.dj import FileField

from .utils import get_extension, encode_url
from .validators import extension_validator, size_validator



class BaseAbstractFile(models.Model):
    file_obj = FileField(verbose_name=_(u'file'), null=True, validators=[extension_validator, size_validator,])
    date_created = models.DateTimeField(_(u'date created'), auto_now_add=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

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
    def file_id(self):
        return self.file_obj.info[u'file_id']

    @property
    def filename(self):
        return self.file_obj.info[u'original_filename'].strip('/')

    @property
    def extension(self):
        return get_extension(self.filename)

    @property
    def size(self):
        return self.file_obj.info[u'size']

    @property
    def mime_type(self):
        return self.file_obj.info[u'mime_type']

    @property
    def is_image(self):
        return self.file_obj.info[u'is_image']

    # And some additional.

    @property
    def is_inline(self):
        return self.extension in settings.INLINE_FILE_FORMATS

    @property
    def is_textual(self):
        max_textfile_size = 1 * 1024 * 1024    # 1 MB.
        return (self.lexer is not None) and self.size <= max_textfile_size

    @property
    def has_preview(self):
        return self.is_image or self.is_textual

    @property
    def pygmented(self):
        if self.is_textual:
            style = styles.get_style_by_name('friendly')
            formatter = formatters.HtmlFormatter(style=style)
            style = formatter.get_style_defs()
            
            file_buffer = urlopen(self.file_obj.cdn_url)

            pygmented_content = u'<style>%s</style>\n' % style
            pygmented_content += highlight(file_buffer.read(), self.lexer, formatter) 
            
            file_buffer.close()
            
            return pygmented_content

    @property
    def lexer(self):
        lexer = getattr(self, '_lexer', None)
        if lexer is None:
            try:
                lexer = lexers.get_lexer_for_filename(self.filename)
            except ClassNotFound:
                lexer = None
            self._lexer = lexer
        return lexer


class File(BaseAbstractFile):

    class Meta:
        verbose_name = _(u'file')
        verbose_name_plural = _(u'files')

    def __unicode__(self):
        return u'%s' % self.file_obj.cdn_url
