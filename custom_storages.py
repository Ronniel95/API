# custom_storages.py
import whitenoise.django
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(whitenoise.django.GzipManifestStaticFilesStorage):
    location = settings.STATICFILES_STORAGE


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION