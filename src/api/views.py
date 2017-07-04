# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# DRF Imports
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Project Imports
from src.profile.models import Profile
from src.profile.serializers import LightProfileSerializer
from src.video.models import Video
from src.video.serializers import VideoSerializer
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

SIX_HOURS_IN_SECONDS = 21600

@api_view(('GET',))
@method_decorator(cache_page(SIX_HOURS_IN_SECONDS))
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def search(request):
    """
    /Search Endpoint implementation.  This endpoint takes 2 query parameters
      category: <int>   -- Category ID of videos to query.
      name: <string>    -- Username to query.

    This endpoint requires either category or name be filled out.
    """
    dict_to_return = {
        'videos': [], 'profiles': []
    }
    category = request.query_params.get('category', False)
    name = request.query_params.get('name', False)

    if category:
        # TODO: Optimize Query and set cache keys
        video_results = Video.objects.filter(category__id=category).select_related('category')
        dict_to_return['videos'] = VideoSerializer(video_results, many=True).data

    if name:
        # TODO: Optimize Query and set cache keys
        profile_results = Profile.objects.filter(username__contains=str(name).lower())
        dict_to_return['profiles'] = LightProfileSerializer(profile_results, many=True).data

    if not category and not name:
        error = {'description': 'You must include either category or name query params'}
        return Response(status=400, data=error)
    return Response(status=200, data=dict_to_return)


