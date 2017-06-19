# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from src.profile.models import Profile
from ..video.models import Video
# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
# 3rd Party Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
# Standard Library Imports
import boto3


class GenerateUploadView(APIView):
    """
    Generate Upload Link and create new video.  The process for this is:
     1. This endpoint is hit
     2. A Video Entry is created and associated with the authenticated user.
     3. An AWS Pre-Signed URL is generated that will allow the consumer of the endpoint to
        post an upload directly to the ranked S3 Upload Bucket.
     4. Final links for fully processed videos are generated.
     [ Outside of the scope of this class - the video will be processed via AWS transcoder and made
       available along with thumbnails ]

    """
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    def post(self, request, format=None):
        try:
            filename = request.data["filename"]
            file_type = request.data["file_type"]
            profile = Profile.objects.get(pk=request.user.id)
            video = Video.objects.create(related_profile=profile, title="", is_processing=True, is_active=False)
            pre_signed_details = video.generate_pre_signed_upload_url(profile.id, filename, file_type)
            # Setup
            video.low = pre_signed_details['low_url']
            video.high = pre_signed_details['final_url']
            video.s3_filename = pre_signed_details['data']['fields']['key']
            video.thumbnail_large, video.thumbnail_small = self.generate_thumbnail_links(video.s3_filename)
            video.save()

            response_dict = {
                'pre_signed_upload_url': pre_signed_details['data']['url'],
                'video_id': video.id,
                'final_url': pre_signed_details['final_url']
            }
            aws_fields = {
                'key': pre_signed_details['data']['fields']['key'],
                'AWSAccessKeyId': pre_signed_details['data']['fields']['AWSAccessKeyId'],
                'Content-Type': file_type,
                'acl': pre_signed_details['data']['fields']['acl'],
                'policy': pre_signed_details['data']['fields']['policy'],
                'signature': pre_signed_details['data']['fields']['signature']
            }
            response_dict['aws_fields'] = aws_fields

            return Response(data=response_dict, status=200)

        # Params missing
        except KeyError as key:
           return Response(data={"description": "Missing Required Field: " + str(key)}, status=410)
        # User doesn't exist
        except ObjectDoesNotExist:
            return Response(data={"description": "Profile not found"}, status=404)


    def generate_thumbnail_links(self, filename):
        STATIC_URL = "https://static.goranked.com"
        try:
            filename_parsed = filename.split('.')[0]
            return ("{}/{}-00001.png".format(STATIC_URL, filename_parsed),
                    "{}/{}-00002.png".format(STATIC_URL, filename_parsed))
        except IndexError:
            return ("", "")


@api_view(['POST',])
def sns_error(request):
    sns_type = request.META['HTTP_X_AMZ_SNS_MESSAGE_TYPE']
    if sns_type == "SubscriptionConfirmation":
        _process_sns_subscription(request)
        return 200
    else:
        return 200

@api_view(['POST',])
def sns_success(request):
    sns_type = request.META['HTTP_X_AMZ_SNS_MESSAGE_TYPE']
    if sns_type == "SubscriptionConfirmation":
        _process_sns_subscription(request)
        return 200
    else:


        return 200


def _process_sns_subscription(request):
    try:
        token = request.data['Token']
        topic = request.data['TopicArn']

        sns_client = boto3.client('sns', region_name='us-west-2')

        response = sns_client.confirm_subscription(
            TopicArn=topic,
            Token=token,
            AuthenticateOnUnsubscribe='false'
        )

    except KeyError as e:
        print("Subscription missing key: {}".format(e))
