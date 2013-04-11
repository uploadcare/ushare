import os

from .base import INSTALLED_APPS, DEBUG



# Uncomment the lines below if you're planning to use AWS S3 file storage.
# Don't forget to install the required packages:
# pip install boto django-storages

# INSTALLED_APPS += ('storages',)

#if not DEBUG:
#    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
#    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
#    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
#    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
#    STATIC_URL = S3_URL
