# Django Imports
from django.core.exceptions import ObjectDoesNotExist
# DRF Imports
from rest_framework.parsers import DjangoMultiPartParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Project Imports
from .models import Profile
from .viewsets import ProfileSerializer
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
import boto3



@api_view(('GET',))
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def me(request):
    try:
        instance = Profile.objects.get(pk=request.user.id)
        return Response(ProfileSerializer(instance=instance,
                                          context={"request": request}).data, status=200)
    except ObjectDoesNotExist:
        Response(status=404)


# Avatar upload View
class AvatarUploadView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None):
        try:
            file_obj = request.data['file']
            filesize_in_kilobytes = file_obj.size / 1000
            file_extension = file_obj.name.split('.')[-1:][0]
            if filesize_in_kilobytes < 1000:
                s3 = boto3.resource('s3')
                profile = Profile.objects.get(pk=request.user.id)
                # TODO: Obviously don't use this naming scheme for production
                s3.Bucket('static.goranked.com').put_object(Key='ava{id}.{ext}'.format(id=profile.id, ext=file_extension),
                                                      Body=file_obj, ACL='public-read')

                # TODO: Hacky - Better way to find extension in production
                profile.avatar_url = "http://static.goranked.com/ava{id}.{ext}".format(id=profile.id, ext=file_extension)
                profile.save()
                return Response(ProfileSerializer(instance=profile,
                                                  context={"request": request}).data, status=200)
            else :
                error = { "description": "Filesize too large! Less than 1MB" }
                return Response(status=304, data=error)
        except ObjectDoesNotExist:
            return Response(status=404)
        except KeyError:
            return Response(status=304)