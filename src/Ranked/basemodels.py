# Django Imports
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
    mobile = models.URLField(default=None, blank=True, null=True)
    low = models.URLField(default=None, blank=True, null=True)
    high = models.URLField(default=None, blank=True, null=True)
    hd = models.URLField(default=None, blank=True, null=True)

    class Meta:
        abstract = True


class Activatable(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class UploadProcessable(models.Model):
    S3_BUCKET = "ranked-video-upload"

    pre_signed_upload_url = models.URLField(default=None, null=True)
    is_processing = models.BooleanField(default=False, db_index=True)
    processing_progress = models.IntegerField(default=0)
    s3_filename = models.CharField(max_length=1024, db_index=True)

    class Meta:
        abstract = True

    def remove_uploaded_file_from_s3(self):
        if self.s3_filename:
            s3 = boto3.resource('s3', region_name="us-west-2")
            bucket = s3.Bucket(name=UploadProcessable.S3_BUCKET)
            bucket.delete_objects(
                Delete={
                    'Objects': [{ 'Key': self.s3_filename }],
                }
            )

    @classmethod
    def generate_pre_signed_upload_url(self, profile_id, filename, file_type):
        s3 = boto3.client('s3', region_name="us-west-2")
        generated_filename = UploadProcessable.get_generated_s3_key(profile_id, filename)

        if not generated_filename:
            return None

        pre_signed_post = s3.generate_presigned_post(
            Bucket=UploadProcessable.S3_BUCKET,
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
            'final_url': 'http://{}/{}'.format("videos.goranked.com", generated_filename),
            'low_url': 'http://{}/{}.webm'.format("videos.goranked.com", generated_filename.split('.')[0])
        }

    @staticmethod
    def get_generated_s3_key(profile_id, filename):
        try:
            # Make sure to only take the characters after the final . in a filename.
            split_filename = filename.split('.')

            if not len(split_filename) > 1:
                return None

            extension = split_filename[-1:][0]
            return "{}-{}.{}".format(profile_id, uuid.uuid4(), extension)
        except IndexError:
            return None

    @staticmethod
    def generate_thumbnail_links(filename):
        STATIC_URL = "http://static.goranked.com"
        try:
            filename_parsed = filename.split('.')[0]
            return ("{}/{}-00001.png".format(STATIC_URL, filename_parsed),
                    "{}/{}-00001.png".format(STATIC_URL, filename_parsed))
        except IndexError:
            return ("", "")


class Rankable(models.Model):
    """
    Rankable content can have a rating
    """
    rank_total = models.IntegerField(default=0)
    is_top_10 = models.BooleanField(default=False, db_index=True)
    top_10_ranking = models.IntegerField(default=None, null=True)

    class Meta:
        abstract = True

    def update_ranking_count(self):
        pass

class CustomFieldStorable(models.Model):
    # Custom_Field 1 is the only field that will be indexed - store things you need to query here.
    custom_field1 = models.CharField(max_length=512, default=None, null=True, db_index=True)
    custom_field2 = models.CharField(max_length=512, default=None, null=True)
    custom_field3 = models.CharField(max_length=512, default=None, null=True)

    class Meta:
        abstract = True
