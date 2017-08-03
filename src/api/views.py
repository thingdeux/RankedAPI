# DRF Imports
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Project Imports
from src.profile.models import Profile
from src.profile.serializers import LightProfileSerializer
from src.video.models import Video
from src.video.serializers import VideoSerializer
from .utils import add_limit_and_offset_to_queryset
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from django.http import HttpResponse
# Django Imports
from django.db.models import Q
from django.views.decorators.cache import cache_page

THREE_HOURS_IN_SECONDS = 10800

# Route "Enums"
SEARCH_ROUTE_BASE = "base"
SEARCH_ROUTE_EXPLORE = "explore"
SEARCH_ROUTE_RANKED_10 = "ranked10"
SEARCH_ROUTE_TRENDING = "trending"
SEARCH_ROUTE_TRENDSETTERS = "trendsetters"

@cache_page(THREE_HOURS_IN_SECONDS)
@api_view(('GET',))
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def search(request, **kwargs):
    dict_to_return = {
        'videos': None, 'profiles': None
    }
    route = kwargs.get('route', 'base')
    category_id = request.query_params.get('category', False)
    name = request.query_params.get('name', False)

    if name and len(name) < 4:
        error = {'description': 'Name cannot be shorter than 3 characters.'}
        return Response(status=400, data=error)

    if route == SEARCH_ROUTE_EXPLORE:
        if not category_id and not name:
            error = {'description': 'Category or name required'}
            return Response(status=400, data=error)
        videos, profiles = __get_explore_data(name, category_id, limit=request.query_params.get('limit', 50),
                                                                 offset=request.query_params.get('offset', None))
        dict_to_return['videos'] = videos
        dict_to_return['profiles'] = profiles
    elif route == SEARCH_ROUTE_RANKED_10:
        dict_to_return['videos'] = VideoSerializer(
            Video.get_ranked_10_videos_queryset(category_id, name, limit=request.query_params.get('limit', 50),
                                                                   offset=request.query_params.get('offset', None)),
                                                                   many=True).data
    elif route == SEARCH_ROUTE_TRENDING:
        dict_to_return['videos'] = VideoSerializer(
            Video.get_ranked_trending_videos_queryset(limit=request.query_params.get('limit', 50),
                                                      offset=request.query_params.get('offset', None)), many=True).data
    elif route == SEARCH_ROUTE_TRENDSETTERS:
        dict_to_return['profiles'] = __get_trendsetters()
    else:
        # Implicit 'base' route - which is category only
        if not category_id:
            error = {'description': 'Category required'}
            return Response(status=400, data=error)
        dict_to_return['videos'] = __get_videos_by_category(category_id,
                                                            limit=request.query_params.get('limit', 50),
                                                            offset=request.query_params.get('offset', None))

    return Response(status=200, data=dict_to_return)

def __get_explore_data(name, category_id, **kwargs):
    # If the name begins with a hashtag (#) then don't include profile results.
    profiles = None
    if name:
        if name[0] != "#":
            profiles = __get_profile_by_name(name)
    videos = __get_explore_search_data(name, category_id, **kwargs)
    return videos, profiles

def __get_videos_by_category(category_id, **kwargs):
    if category_id:
        results = Video.objects.filter(category__id=category_id, is_active=True).select_related('category')\
            .select_related('related_profile').select_related('category').select_related('category__parent_category')
        results = add_limit_and_offset_to_queryset(results, **kwargs)

        return VideoSerializer(results, many=True).data
    else:
        return None

def __get_explore_search_data(filter_phrase, category_id, **kwargs):
    base_queryset = Video.get_videos_performant_queryset()
    base_queryset = base_queryset.filter(is_active=True)

    if category_id:
        base_queryset = base_queryset.filter(Q(category__id=category_id) | Q(category__parent_category__id=category_id))

    if filter_phrase:
        # Add the trailing comma for accuracy, ex: if I search for BestNBA or BestNBADunks without the
        # Trailing comma ending the phrase they'll both return the same videos.
        base_queryset = base_queryset.filter(hashtag__icontains=str(filter_phrase + ","))
    base_queryset = add_limit_and_offset_to_queryset(base_queryset, **kwargs)
    return VideoSerializer(base_queryset[:50], many=True).data

def __get_profile_by_name(name, **kwargs):
    queryset = Profile.objects.filter(username__icontains=name, is_active=True)
    queryset = add_limit_and_offset_to_queryset(queryset, **kwargs)
    return LightProfileSerializer(queryset, many=True).data


def __get_trendsetters():
    return LightProfileSerializer(Profile.get_trend_setters_queryset(), many=True).data

# Health Check endpoint for ELB
def health_check(request):
    return HttpResponse(status=200)