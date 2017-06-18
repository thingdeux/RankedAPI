from django.db import models
# Standard Library imports
import json
import uuid
import boto3

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
    thumbnail_large = models.URLField(default=None, null=True)
    thumbnail_small = models.URLField(default=None, null=True)

    class Meta:
        abstract = True


class MultipleQualityLinkable(models.Model):
    mobile = models.URLField(default=None, null=True)
    low = models.URLField(default=None, null=True)
    high = models.URLField(default=None, null=True)
    hd = models.URLField(default=None, null=True)

    class Meta:
        abstract = True


class Activatable(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class UploadProcessable(models.Model):
    pre_signed_upload_url = models.URLField(default=None, null=True)
    is_processing = models.BooleanField(default=False, db_index=True)
    processing_progress = models.IntegerField(default=0)
    s3_filename = models.CharField(max_length=1024,default=None, null=True)

    class Meta:
        abstract = True

    @classmethod
    def generate_pre_signed_upload_url(self, profile_id, filename, file_type):
        S3_BUCKET = "ranked-video-upload"
        s3 = boto3.client('s3')
        generated_filename = "{}-{}-{}".format(profile_id, uuid.uuid4(), filename)

        pre_signed_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=generated_filename,
            Fields={"acl": "bucket-owner-full-control", "Content-Type": file_type},
            Conditions=[
                {"acl": "bucket-owner-full-control"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )

        return {
            'data': pre_signed_post,
            'final_url': 'https://%s/%s' % ("videos.goranked.com", generated_filename)
        }