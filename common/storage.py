"""
Cloudflare R2 storage configuration.
"""

from django.conf import settings
from django.core.files.storage import Storage
from storages.backends.s3boto3 import S3Boto3Storage


class R2StaticStorage(S3Boto3Storage):
    """Storage class for static files on Cloudflare R2."""

    location = "static"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False


class R2MediaStorage(S3Boto3Storage):
    """Storage class for media files on Cloudflare R2."""

    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False


def get_storage_backend() -> Storage:
    """Get the appropriate storage backend based on configuration."""
    if settings.USE_S3:
        return R2MediaStorage()
    from django.core.files.storage import default_storage

    return default_storage
