from short_url import UrlEncoder

from django.conf import settings



URL_ENCODER = UrlEncoder(settings.SHORT_URL_ALPHABET, settings.SHORT_URL_BLOCK_SIZE)


def encode_url(n):
    return URL_ENCODER.encode_url(n, settings.SHORT_URL_MIN_LENGTH)


def decode_url(n):
    return URL_ENCODER.decode_url(n)


def get_extension(filename):
    try:
        ext = filename.rsplit('.', 1)[1]
    except IndexError:
        ext = u''
    return ext
