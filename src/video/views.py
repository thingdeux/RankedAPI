# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from src.profile.models import Profile
from ..video.models import Video
from ..video.sns import SNSResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import BaseParser
from rest_framework.parsers import JSONParser, FormParser
# 3rd Party Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
# Standard Library Imports
import boto3
import json
import logging


logger = logging.getLogger("video.views")
SIX_HOURS_IN_SECONDS = 21600

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


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
    parser_classes = ([JSONParser, FormParser])

    def post(self, request, format=None):
        try:
            filename = request.data["filename"]
            file_type = request.data["file_type"]
            profile = Profile.objects.get(pk=request.user.id)
            pre_signed_details = Video.generate_pre_signed_upload_url(profile.id, filename, file_type)

            if not pre_signed_details:
                error = {"description": 'Filename is not acceptable'}
                return Response(status=400, data=error)

            # Setup Video DB Entry
            video = Video.objects.create(related_profile=profile, title="", is_processing=True,
                                         is_active=False, s3_filename=pre_signed_details['data']['fields']['key'])

            video.low = pre_signed_details['low_url']
            video.high = pre_signed_details['final_url']
            video.thumbnail_large, video.thumbnail_small = Video.generate_thumbnail_links(video.s3_filename)
            video.pre_signed_upload_url = pre_signed_details['data']['url']
            video.save()

            response_dict = {
                'pre_signed_upload_url': pre_signed_details['data']['url'],
                'video_id': video.id,
                'final_url': pre_signed_details['final_url']
            }
            response_dict['aws_fields'] = pre_signed_details['data']['fields']

            return Response(data=response_dict, status=200)

        # Params missing
        except KeyError as key:
           return Response(data={"description": "Missing Required Field: " + str(key)}, status=410)
        # User doesn't exist
        except ObjectDoesNotExist:
            return Response(data={"description": "Profile not found"}, status=404)


# SNS Handlers
@api_view(['POST',])
@parser_classes([PlainTextParser,])
def sns_error(request):
    sns_type = request.META['HTTP_X_AMZ_SNS_MESSAGE_TYPE']
    if sns_type == "SubscriptionConfirmation":
        json_data = json.loads(str(request.data, 'utf-8'))
        __process_sns_subscription(json_data)
        return Response(status=200)
    else:
        response = SNSResponse(request.data)
        logger.error("AWS Error processing job id: {}", response.job_id)
        # TODO: Should probably put this on celery
        related_video = Video.objects.get(s3_filename=response.processed_filename)
        related_video.is_processing = False
        related_video.deactivate()
        # TODO: Maybe try re-doing the transcode at a later time - for now fail.

        return Response(status=200)


@api_view(['POST',])
@parser_classes([PlainTextParser,])
def sns_success(request):
    sns_type = request.META['HTTP_X_AMZ_SNS_MESSAGE_TYPE']
    if sns_type == "SubscriptionConfirmation":
        json_data = json.loads(str(request.data, 'utf-8'))
        __process_sns_subscription(json_data)
        return Response(status=200)
    else:
        response = SNSResponse(request.data)
        logger.info("AWS Successfully processed job id: {}", response.job_id)
        # TODO: Should probably put this on celery
        try:
            related_video = Video.objects.get(s3_filename=response.processed_filename)
            related_video.is_processing = False
            related_video.activate()

            try:
                related_video.remove_uploaded_file_from_s3()
            except Exception as error:
                logger.error("Error Deleting S3 File: {}".format(error))

            return Response(status=200)
        except ObjectDoesNotExist:
            logger.error("Unable to find video for key: {}".format(response.processed_filename))
            return Response(status=200)



# PRIVATE HELPERS
def __process_sns_subscription(json_data):
    try:
        token = json_data['Token']
        topic = json_data['TopicArn']
        sns_client = boto3.client('sns', region_name='us-west-2')

        sns_client.confirm_subscription(
            TopicArn=topic,
            Token=token,
            AuthenticateOnUnsubscribe='false'
        )

    except KeyError as e:
        print("Subscription missing key: {}".format(e))




