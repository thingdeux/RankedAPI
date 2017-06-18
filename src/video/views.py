# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from src.profile.models import Profile
from ..video.models import Video
# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# 3rd Party Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
# Standard Library Imports
import json


#Generate Video Presigned Note
class GenerateUploadView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    def post(self, request, format=None):
        try:
            filename = request.data["filename"]
            file_type = request.data["file_type"]
            profile = Profile.objects.get(pk=request.user.id)
            video = Video.objects.create(related_profile=profile, title="", is_processing=True, is_active=False)
            pre_signed_details = video.generate_pre_signed_upload_url(profile.id, filename, file_type)
            video.s3_filename = pre_signed_details['data']['fields']['key']
            video.save()

            response_dict = {
                'pre_signed_upload_url': pre_signed_details['data']['url'],
                'video_id': video.id,
                'final_url': pre_signed_details['final_url']
            }
            aws_fields = {
                'key': pre_signed_details['data']['fields']['key'],
                'AWSAccessKeyId': pre_signed_details['data']['fields']['AWSAccessKeyId'],
                'acl': pre_signed_details['data']['fields']['acl'],
                'policy': pre_signed_details['data']['fields']['policy'],
                'signature': pre_signed_details['data']['fields']['signature'],
                'Content-Type': file_type
            }
            response_dict['aws_fields'] = aws_fields

            return Response(data=response_dict, status=200)

        # Params missing
        except KeyError as key:
           return Response(data={"description": "Missing Required Field: " + str(key)}, status=410)
        # User doesn't exist
        except ObjectDoesNotExist:
            return Response(data={"description": "Profile not found"}, status=404)
