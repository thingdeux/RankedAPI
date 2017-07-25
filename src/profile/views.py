# Django Imports
from django.core.exceptions import ObjectDoesNotExist
# DRF Imports
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Project Imports
from .models import Profile
from src.video.models import Video
from src.video.serializers import VideoSerializer
from .viewsets import ProfileSerializer
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
import boto3
import uuid

@api_view(('GET',))
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def me(request):
    try:
        profile = Profile.objects.filter(pk=request.user.id).select_related('primary_category')\
            .select_related('primary_category__parent_category').select_related('secondary_category')\
            .select_related('secondary_category__parent_category').first()
        videos = Video.objects.filter(related_profile=profile).select_related('related_profile')\
            .select_related('category').select_related('category__parent_category')

        my_ranked_videos = [x['id'] for x in Video.get_all_videos_user_has_ranked_queryset(profile.id)]

        response_dict = {
            'me': ProfileSerializer(instance=profile, context={"request": request}).data,
            'videos': VideoSerializer(instance=videos, many=True).data,
            'my_ranked_video_ids': my_ranked_videos
        }
        return Response(data=response_dict, status=200)
    except ObjectDoesNotExist:
        Response(status=404)


# Avatar upload View
class AvatarUploadView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, format=None):
        try:
            file_obj = request.data['file']
            filesize_in_kilobytes = file_obj.size / 1000
            file_extension = file_obj.name.split('.')[-1:][0]
            # Anything larger than 8MB's gets turned away
            if filesize_in_kilobytes < 8100:
                s3 = boto3.resource('s3')
                profile = Profile.objects.get(pk=request.user.id)
                generated_s3_key = 'ava{id}-{uuid}.{ext}'.format(id=profile.id, uuid=uuid.uuid4(), ext=file_extension)
                s3.Bucket('static.goranked.com').put_object(Key=generated_s3_key, Body=file_obj, ACL='public-read')

                profile.avatar_url = "http://static.goranked.com/{}".format(generated_s3_key)
                profile.save()
                return Response(ProfileSerializer(instance=profile,
                                                  context={"request": request}).data, status=200)
            else :
                error = { "description": "Filesize too large! Less than 1MB" }
                return Response(status=413, data=error)
        except ObjectDoesNotExist:
            return Response(status=404)
        except KeyError:
            error = {"description": "'File' parameter missing"}
            return Response(status=304, data=error)