# DRF Imports
from rest_framework import permissions, routers, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from .serializers import ProfileSerializer, LightProfileSerializer
# Project Imports
from .models import Profile
from src.video.models import Video
from src.video.serializers import VideoSerializer
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# Django Imports
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # TODO: Password update - should hash.

    def retrieve(self, request, *args, **kwargs):
        try:
            # TODO: JJ - Performance Gains from query optimization on this reverse lookup.
            profile = Profile.objects.get(pk=kwargs['pk'])
            videos = Video.objects.filter(related_profile=profile)

            response_dict = {
                'me': LightProfileSerializer(instance=profile, context={"request": request}).data,
                'videos': VideoSerializer(instance=videos, many=True).data
            }
            return Response(data=response_dict, status=200)
        except ObjectDoesNotExist:
            Response(status=404)
        except KeyError:
            Response(status=404)



# Viewset for /users/register endpoint.
class RegisterViewSet(viewsets.ModelViewSet):
    """
    Viewset for User Registration
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        try:
            # Get e-mail post param
            # Make sure e-mail doesn't already exist
            serialized_profile = ProfileSerializer(data=request.data)
            _validate_registration_fields(request.data)
            if serialized_profile.is_valid():
                existing_account = list(Profile.objects.filter(email=serialized_profile.validated_data['email']))

                if len(existing_account) > 0:
                    error = {"description": "E-Mail already exists"}
                    return Response(status=408, data=error)

                new_profile = serialized_profile.save()
                new_profile.save()
                serialized_new_profile = ProfileSerializer(new_profile)

                return Response(status=201, data=serialized_new_profile.data)
            else:
                errors = []
                for error in serialized_profile.errors:
                    errors.append(error)

                error = { "description": "Errors in fields", "errors": errors }
                return Response(status=400, data=error)
        except KeyError as e:
            error = {"description": "Not sending over proper values {}".format(e)}
            return Response(status=400, data=error)
        except ValidationError:
            error = { "description": "Password does not meet standards. At least 6 characters.", "errors": ["password"]}
            return Response(status=400, data=error)

def _validate_registration_fields(data):
    validate_password(data['password'])
    _ = data['username']
    _ = data['unlock_key']
    _ = data['email']