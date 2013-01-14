from django.core.exceptions import ValidationError
from django.conf import settings

from .utils import get_extension



def extension_validator(value):
    extension = get_extension(value.info[u'original_filename'])
    allowed_extensions = getattr(settings, 'ALLOWED_EXTENSIONS', ())
    forbidden_extensions = getattr(settings, 'FORBIDDEN_EXTENSIONS', ())

    if extension in forbidden_extensions or (allowed_extensions and extension not in allowed_extensions):
        raise ValidationError(u'".%s" is not a permitted file extension.' % extension)


def size_validator(value):
    max_file_size = getattr(settings, 'MAX_FILE_SIZE', 100 * 1024 * 1024)
    file_size = value.info[u'size']
    if file_size > max_file_size:
        raise ValidationError(u'File size can not exceed %i bytes.' % max_file_size)
