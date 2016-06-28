from urllib import urlopen
from markdown import markdown
from textile import textile
from pygments import lexers, formatters, highlight, styles
from pygments.util import ClassNotFound

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.encoding import iri_to_uri

from pyuploadcare.dj.models import FileField

from .utils import get_extension, encode_url
from .validators import extension_validator, size_validator


TEXTILE_FILE_EXTENSIONS = ('textile',)
MARKDOWN_FILE_EXTENSIONS = ('md',)
MAX_TEXTFILE_SIZE = 1 * 1024 * 1024


class BaseAbstractFile(models.Model):
    file_obj = FileField(verbose_name=_(u'file'),
                         null=True,
                         validators=[extension_validator, size_validator])
    date_created = models.DateTimeField(_(u'date created'),
                                        auto_now_add=True,
                                        null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

    @models.permalink
    def get_absolute_url(self):
        return ('files:detail', (self.encoded_id,))

    def url(self, use_https=False):
        mapping = {
            'protocol': 'https' if use_https else 'http',
            'domain': Site.objects.get_current().domain,
            'url': self.get_absolute_url(),
            'filename': self.filename,
        }
        return iri_to_uri(u'%(protocol)s://%(domain)s%(url)s%(filename)s' % mapping)

    @property
    def encoded_id(self):
        return encode_url(self.id)

    # A bunch of proxy-methods.

    @property
    def file_id(self):
        return self.file_obj.info()[u'file_id']

    @property
    def filename(self):
        return self.file_obj.info()[u'original_filename'].strip('/').replace('/', '_')

    @property
    def extension(self):
        return get_extension(self.filename)

    @property
    def size(self):
        return self.file_obj.info()[u'size']

    @property
    def mime_type(self):
        return self.file_obj.info()[u'mime_type']

    @property
    def is_image(self):
        return self.file_obj.info()[u'is_image']

    # And some additional.

    @property
    def is_inline(self):
        return self.extension in settings.INLINE_FILE_FORMATS

    @property
    def text_content(self):
        if self.size <= MAX_TEXTFILE_SIZE and not self.is_image:
            possible_markdown = self.extension in (MARKDOWN_FILE_EXTENSIONS +
                                                   TEXTILE_FILE_EXTENSIONS)
            fake_extension = self.extension if not possible_markdown else u'txt'
            fake_filename = u'.'.join((self.filename, fake_extension,))

            style = styles.get_style_by_name('friendly')
            formatter = formatters.HtmlFormatter(style=style)
            style = formatter.get_style_defs()

            f = urlopen(self.file_obj.cdn_url)
            data = f.read()
            f.close()

            try:
                data = data.decode('utf-8')
                lexer = lexers.guess_lexer_for_filename(fake_filename, data)
            except (ClassNotFound, UnicodeDecodeError):
                return None

            if isinstance(lexer, lexers.TextLexer) and possible_markdown:
                format_string = u'<div class="%s">%s</div>'

                if self.extension in MARKDOWN_FILE_EXTENSIONS:
                    data = format_string % ('markdown', markdown(data))

                if self.extension in TEXTILE_FILE_EXTENSIONS:
                    data = format_string % ('textile', textile(data))

            else:
                data = u'<style>%s</style>\n%s' % (style, highlight(data, lexer, formatter))

            return data


class File(BaseAbstractFile):

    class Meta:
        verbose_name = _(u'file')
        verbose_name_plural = _(u'files')

    def __unicode__(self):
        return u'%s' % self.file_obj.cdn_url
