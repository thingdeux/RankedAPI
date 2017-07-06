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

# Route "Enums"
SEARCH_ROUTE_BASE = "base"
SEARCH_ROUTE_EXPLORE = "explore"
SEARCH_ROUTE_RANKED_10 = "ranked10"
SEARCH_ROUTE_TRENDING = "trending"
SEARCH_ROUTE_TRENDSETTERS = "trendsetters"

@api_view(('GET',))
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def search(request, **kwargs):
    dict_to_return = {
        'videos': None, 'profiles': None
    }
    route = kwargs.get('route', 'base')
    category_id = request.query_params.get('category', False)
    name = request.query_params.get('name', False)

    if route == SEARCH_ROUTE_EXPLORE:
        # If the name begins with a hashtag (#) then don't include profile results.
        if name:
            if name[0] != "#":
                dict_to_return['profiles'] = __get_profile_by_name(name)
            dict_to_return['videos'] = __get_explore_search_data(name, category_id)

    elif route == SEARCH_ROUTE_RANKED_10:
        dict_to_return['videos'] = Video.get_ranked_10_videos_queryset(name)
    elif route == SEARCH_ROUTE_TRENDING:
        dict_to_return['videos'] = Video.get_ranked_trending_videos_queryset()
    elif route == SEARCH_ROUTE_TRENDSETTERS:
        dict_to_return['profiles'] = Profile.get_trend_setters_queryset()
    else:
        # Implicit 'base' route - which is category only
        if not name:
            error = {'description': 'Category required'}
            return Response(status=400, data=error)
        dict_to_return['videos'] = __get_videos_by_category()

    return Response(status=200, data=dict_to_return)

def __get_videos_by_category(category_id):
    if category_id:
        return Video.objects.filter(category__id=category_id, is_active=True).select_related('category')\
            .select_related('related_profile')
    else:
        return None

def __get_explore_search_data(filter_phrase=None, category_id=None):
    base_queryset = Video.objects.filter(is_active=True)

    if category_id:
        base_queryset.filter(category__id=category_id).select_related('category').select_related('related_profile')
    if filter_phrase:
        base_queryset.filter(title__icontains=str(filter_phrase))
    return VideoSerializer(base_queryset, many=True).data

def __get_profile_by_name(name):
    return LightProfileSerializer(Profile.objects.filter(username__icontains=name, is_active=True), many=True).data
