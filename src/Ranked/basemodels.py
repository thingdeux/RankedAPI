from django.db import models

class Base(models.Model):
    """
    a base object for all ORM database models to inherit from, for extra metadata
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hashtagable(models.Model):
    hashtag = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class ThumbnailDisplayable(models.Model):
    thumbnail_large = models.URLField(default=None)
    thumbnail_small = models.URLField(default=None)

    class Meta:
        abstract = True


class MultipleQualityLinkable(models.Model):
    mobile = models.URLField(default=None)
    low = models.URLField(default=None)
    high = models.URLField(default=None)
    hd = models.URLField(default=None)

    class Meta:
        abstract = True


class UploadProcessable(models.Model):
    pre_signed_upload_url = models.URLField(default=None, null=True)

    class Meta:
        abstract = True

    def generate_pre_signed_upload_url(self, for_type="video"):
        pass