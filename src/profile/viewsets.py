# DRF Imports
from rest_framework import permissions, routers, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from .serializers import ProfileSerializer
# Project Imports
from .models import Profile
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# Django Imports
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


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
                new_profile.set_password(serialized_profile['password'])
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
    username = data['username']
    access_code = data['unlock_key']
    email = data['email']