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

#Generate Video Presigned Note
class GenerateUploadView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    def create(self, request, format=None):
        try:
            filename = request.data["filename"]
            file_type = request.data["file_type"]
            profile = Profile.objects.get(pk=request.user.id)
            video = Video.objects.create(profile=profile, title="", is_processing=True)
            pre_signed_details = video.generate_pre_signed_upload_url(profile.id, filename, file_type)
            video.s3_filename = pre_signed_details['data']['Key']

            return Response(data=pre_signed_details, status=200)

        # Params missing
        except KeyError as key:
           return Response(data={"description": "Missing Required Field: " + str(key)}, status=410)
        # User doesn't exist
        except ObjectDoesNotExist:
            pass
