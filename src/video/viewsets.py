# DRF Imports
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Project Imports
from src.comment.serializers import CommentSerializer
from .models import Video
from src.ranking.models import Ranking
from src.comment.models import Comment
from src.categorization.models import Category
from src.profile.serializers import LightProfileSerializer, BasicProfileSerializer
from .serializers import VideoSerializer
from src.profile.models import Profile
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.core.exceptions import ObjectDoesNotExist
import re
# Django Imports
from django.db import transaction

class VideoViewSet(viewsets.ModelViewSet):
    """
    Viewset for Videos
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    parser_classes = (FormParser, JSONParser)
    ordering_fields = ()

    def retrieve(self, request, *args, **kwargs):
        video_id = kwargs.get('pk', None)
        try:
            if video_id:
                video = Video.objects.filter(id=video_id)\
                    .prefetch_related('comments').select_related('category').select_related('category__parent_category')\
                    .select_related('related_profile').first()

                if not video:
                    raise ObjectDoesNotExist

                video_serialized = VideoSerializer(video)
                profile_serialized = BasicProfileSerializer(video.related_profile)
                comments_serialized = CommentSerializer(video.comments, many=True)

                # TODO: Profile this query - gonna be gnarly

                to_return = video_serialized.data
                to_return['uploaded_by'] = profile_serialized.data
                to_return['comments'] = comments_serialized.data

                return Response(status=200, data=to_return)
        except ObjectDoesNotExist:
            return Response(status=404)

    def list(self, request, *args, **kwargs):
        try:
            queryset = Video.get_videos_from_profiles_user_follows_queryset(request.user.id,
                                                                            request.query_params.get('limit', None),
                                                                            request.query_params.get('offset', None))


            serialized = VideoSerializer(queryset, many=True)
            return Response(status=200, data=serialized.data)
        except ValueError:
            error = {'description': 'There was a problem reading your request.'}
            return Response(status=400, data=error)

    def create(self, request, *args, **kwargs):
        error = {"description":  "POST to /videos/ is not how videos are created. Please see documentation."}
        return Response(status=505, data=error)

    def update(self, request, *args, **kwargs):
        try:
            self.__update_video(kwargs['pk'], request.data)
            return Response(status=200)
        except KeyError as e:
            return Response(status=400)
        except ObjectDoesNotExist:
            return Response(status=404)

    @detail_route(methods=['post'], permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope])
    def viewed(self, request, pk=None):
        try:
            if not pk:
                error = {'description': 'Video ID Required'}
                return Response(status=400, data=error)
            video = Video.objects.get(pk=pk)
            with transaction.atomic():
                video.views += 1
                video.save()
        except ObjectDoesNotExist:
            error = {'description': 'Video does not exist'}
            return Response(status=400, data=error)

        return Response(status=200)

    @detail_route(methods=['post', 'delete'], permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope])
    def rank(self, request, pk=None):
        """
        Handle Video Ranking
        POST: Rank a video on a scale between 1-10
        DELETE: Remove Ranking for authorized user
        """
        if request.method == "POST":
            try:
                video = Video.objects.get(id=pk)
                profile = self.request.user
                rank_amount = VideoViewSet.__get_rank_as_int(request.data.get('rank_amount', 1))

                if rank_amount > 10:
                    rank_amount = 10
                elif rank_amount < 1:
                    rank_amount = 1

                new_rank, was_created = Ranking.objects.get_or_create(related_profile=profile, video=video)
                if was_created:
                    new_rank.rank_amount = rank_amount
                    new_rank.save()
                    return Response(status=200, data={'description': 'Success'})
                else:
                    return Response(status=304, data={'description': 'This video has already been ranked'})
            except ObjectDoesNotExist:
                error = {"description": "Video Not Found"}
                return Response(status=404, data=error)
        elif request.method == "DELETE":
            return self.__delete_ranking(self.request.user, pk)

    @staticmethod
    def __get_rank_as_int(amount):
        try:
            return int(amount)
        except ValueError:
            return 1

    def __delete_ranking(self, profile, video_id):
        try:
            profile = self.request.user
            video = Video.objects.get(id=video_id)
            latest_ranking = Ranking.objects.get(video=video, related_profile=profile)
            latest_ranking.delete()
            return Response(status=200, data={'description': 'Success'})
        except ObjectDoesNotExist:
            error = {"description": "No Ranking Found for Profile"}
            return Response(status=404, data=error)

    @detail_route(methods=['post'], permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope])
    def comments(self, request, pk=None):
        """
        Handle Video Commenting
        POST: Comment on a video
        """
        try:
            comment = request.data['comment']

            if len(comment) > 512:
                return Response(status=400, data={'description': 'Comment Length exceeds 512 characters'})
            elif len(comment) < 1:
                raise ValueError
            else:
                video = Video.objects.get(id=pk)
                profile = self.request.user
                new_comment = Comment.objects.create(related_profile=profile, video=video, text=comment)
                new_comment.save()
                return Response(status=200, data={'description': 'Success'})

        except ObjectDoesNotExist:
            return Response(status=404, data={"description": "Video Not Found"})
        except (KeyError, ValueError):
            return Response(status=400, data={'description': 'Comment Length too short'})

    def __update_video(self, video_id, request_data):
        video = Video.objects.get(pk=video_id)

        if request_data.get('title', False):
            video.title, video.hashtag = VideoViewSet.__extract_hashtags(request_data['title'])
        else:
            video.title = video.title

        category = request_data.get('category', False)

        if category:
            new_category = Category.objects.get(id=category)
            video.category = new_category

        video.save()

    @staticmethod
    def __extract_hashtags(title: str):
        """
        Extract hashtags from title.

        Supported formats:
         [Space Delineation] ex: #Sweet #Noice #Totes
         [Comma Delineation] ex: #Sweet,#Noice,#Totes
         [Just hashes Delineation] ex: #Sweet#Noice#Totes

        :return: Tuple (Title Stripped of hashtags, hashtags comma delimited
        """
        # TODO: Logic is fairly gnarly but it gets the job done. Would like more safety for edge cases.
        hashtag_finder = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)

        final_title = None
        hashtags = ""

        for text in hashtag_finder.split(title):
            if len(text) < 1:
                continue

            word_count = text.split(' ')

            if len(word_count) > 1 and not final_title:
                final_title = text.rstrip(' ')
            else:
                # If there are no spaces between hashtags the regex will combine multiple hashtags in one string
                # Split that and parse it.
                if text.startswith('#'):
                    for bound_hashtag in text.split('#'):
                        if len(bound_hashtag) > 1:
                            hashtags = hashtags + ",#" + bound_hashtag
                    continue

                if len(hashtags) < 1:
                    hashtags = "#" + text
                    continue
                hashtags = hashtags + ",#" + text

        return final_title or "", hashtags

# Avatar upload View
class VideoTopView(APIView):
    SIX_HOURS_IN_SECONDS = 21600
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @method_decorator(cache_page(SIX_HOURS_IN_SECONDS))
    def get(self, request, format=None):
        queryset = Video.objects.order_by('-rank_total').filter(is_active=True).select_related('related_profile') \
            .select_related('related_profile').select_related('related_profile__secondary_category') \
            .select_related('related_profile__primary_category').select_related(
            'related_profile__primary_category__parent_category') \
            .select_related('related_profile__secondary_category__parent_category').select_related('category')\
            .select_related('category__parent_category')[:25]
        serialized = VideoSerializer(queryset, many=True)
        return Response(serialized.data)