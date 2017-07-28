# DRF Imports
from rest_framework import permissions, routers, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from .serializers import ProfileSerializer, LightProfileSerializer, BasicProfileSerializer
from rest_framework.decorators import detail_route
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
from django.db.utils import IntegrityError

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().prefetch_related('primary_category', 'secondary_category')


    def list(self, request, *args, **kwargs):
        error = {'description': 'Not Available'}
        return Response(status=405, data=error)

    def update(self, request, *args, **kwargs):
        try:
            if int(kwargs['pk']) == request.user.id:
                # Only a couple of fields are editable - the following can be updated.
                # phone_number | email | password
                profile = Profile.objects.get(pk=request.user.id)
                profile.email = request.data.get('email', profile.email)
                profile.phone_number = request.data.get('phone_number', profile.phone_number)

                new_password = request.data.get('password', False)
                # Make sure password can be saved before attempting to even save it.
                # Make sure to read the method description for validate_password - none == A-Ok
                if new_password and not validate_password(new_password):
                    profile.set_password(new_password)

                profile.save()
                return Response(status=200)
            else:
                error = {"description": "You do not have access to edit this account."}
                return Response(status=401, data=error)
        except ObjectDoesNotExist:
            return Response(status=404)
        except ValidationError:
            error = {"description": "Password does not meet standards. At least 6 characters.",
                     "errors": ["password"]}
            return Response(status=400, data=error)
        except IntegrityError:
            error = {'description': 'E-Mail already in use'}
            return Response(status=408, data=error)
        except KeyError:
            return Response(status=404)

    def retrieve(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.filter(pk=kwargs['pk']).select_related('primary_category')\
            .select_related('primary_category__parent_category').select_related('secondary_category')\
            .select_related('secondary_category__parent_category').first()
            videos = Video.objects.filter(related_profile=profile).select_related('related_profile') \
                .select_related('category').select_related('category__parent_category')

            response_dict = {
                'user': LightProfileSerializer(instance=profile, context={"request": request}).data,
                'videos': VideoSerializer(instance=videos, many=True).data
            }
            return Response(data=response_dict, status=200)
        except ObjectDoesNotExist:
            Response(status=404)
        except KeyError:
            Response(status=404)

    @detail_route(methods=['post', 'delete', 'get'], permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope])
    def following(self, request, pk=None):
        """
        Follow a user
        GET: List profiles user is following
        POST: Follow the user passed in {pk} with the currently authenticated account.
        DELETE: Stop following the user passed in {pk} with the currently authenticated account.
        """
        if request.method == "GET":
            try:
                return _get_profiles_user_is_following(pk)
            except ObjectDoesNotExist as e:
                error = {"description": "Profile not found {}".format(e)}
                Response(status=404, data=error)
        else:
            profile = Profile.objects.filter(id=request.user.id).only('id').first()
            try:
                if request.method == "POST":
                    profile.follow_user(pk)
                    profile.save()
                    return Response(status=200)
                elif request.method == "DELETE":
                    profile.stop_following_user(pk)
                    profile.save()
                    return Response(status=200)
            except ObjectDoesNotExist as e:
                error = {"description": "Profile not found {}".format(e)}
                return Response(status=404, data=error)

    @detail_route(methods=['get'], permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope])
    def followers(self, request, pk=None):
        """
        Follow a user
        GET: List profiles following a given user
        """
        try:
            return _get_profiles_following_user(pk)
        except ObjectDoesNotExist as e:
            error = {"description": "Profile not found {}".format(e)}
            Response(status=404, data=error)


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
                new_profile = serialized_profile.save()
                new_profile.save()
                serialized_new_profile = ProfileSerializer(new_profile)

                return Response(status=201, data=serialized_new_profile.data)
            else:
                errors = []
                for error in serialized_profile.errors:
                    errors.append(error)
                if 'email' in errors:
                    error = {"description": "E-Mail already exists"}
                    return Response(status=408, data=error)

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

def _get_profiles_user_is_following(profile_id):
    profile = Profile.objects.filter(id=profile_id).prefetch_related('followed_profiles').first()
    followed_profiles = list(profile.followed_profiles.all())

    if len(followed_profiles) > 0:
        return Response(status=200, data={
            'users': BasicProfileSerializer(followed_profiles, many=True).data
        })
    else:
        return Response(status=200, data={'users': []})


def _get_profiles_following_user(profile_id):
    followers = Profile.objects.filter(followed_profiles__id=profile_id).prefetch_related('followed_profiles')\
    .select_related('primary_category').select_related('primary_category__parent_category')\
    .select_related('secondary_category').select_related('secondary_category__parent_category')
    followed_profiles = list(followers)

    if len(followed_profiles) > 0:
        return Response(status=200, data={
            'users': BasicProfileSerializer(followed_profiles, many=True).data
        })
    else:
        return Response(status=200, data={'users': []})