import boto3
from botocore.exceptions import ClientError
from .raw_input_data import names_to_purge

class UploadPurger:
    """
    Class for fully purging video uploads

    Will run delete operations for these S3 Buckets

    videos.goranked.com  |  webm, mp4 extensions
    static.goranked.com  |  jpg, png extensions and walk 0000[X]
    ranked-video-upload  |  file_key*
    """
    def __init__(self):
        self.init_s3_client()
        self.files_to_process = self.parse_raw_input()

    def parse_raw_input(self):
        to_return = []
        for filename in names_to_purge.split('\n'):
            if len(filename) > 0:
                to_return.append(filename)
        return to_return

    def process(self):
        for filename in self.files_to_process:
            # Delete jpg thumbnails
            self.delete_from_s3('static.goranked.com', '{}-00001.jpg'.format(filename))
            self.delete_from_s3('static.goranked.com', '{}-lrg-00001.jpg'.format(filename))
            # Delete any old-style png thumbnails
            self.delete_from_s3('static.goranked.com', '{}-00001.png'.format(filename))
            self.delete_from_s3('static.goranked.com', '{}-00002.png'.format(filename))
            self.delete_from_s3('static.goranked.com', '{}-00003.png'.format(filename))
            self.delete_from_s3('videos.goranked.com', '{}.webm'.format(filename))
            self.delete_from_s3('videos.goranked.com', '{}.mp4'.format(filename))

    def init_s3_client(self):
        try:
            self.s3_client = boto3.client('s3')
        except ClientError as err:
            print("Failed to create boto3 client.\n" + str(err))
            return False

    def delete_from_s3(self, bucket_name, file_key):
        """
        Uploads an artifact to Amazon S3
        """
        try:
            response = self.s3_client.delete_object(
                Bucket=bucket_name,
                Key=file_key
            )
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            if status_code != 204:
                print("Deleted: {} ? - {}".format(file_key, status_code))
        except ClientError as err:
            print("Received S3 Client Error {}".format(err))

def update_videos_to_large_urls():
    from django.core.exceptions import ObjectDoesNotExist
    from src.video.models import Video

    for filename in names_to_purge.split('\n'):
        if len(filename) > 0:
            vid_to_update = None

            try:
                vid_to_update = Video.objects.get(custom_field1='{}.mp4'.format(filename))
            except ObjectDoesNotExist:
                vid_to_update = Video.objects.filter(custom_field1='{}.mov'.format(filename)).first()
            finally:
                if vid_to_update:
                    vid_to_update.thumbnail_large = 'http://static.goranked.com/{}-lrg-00001.jpg'.format(filename)
                    vid_to_update.save()
