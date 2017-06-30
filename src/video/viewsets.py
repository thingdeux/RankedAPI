# DRF Imports
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import detail_route
# Project Imports
from src.comment.serializers import CommentSerializer
from .models import Video
from src.ranking.models import Ranking
from src.comment.models import Comment
from src.categorization.models import Category
from src.profile.serializers import LightProfileSerializer
from .serializers import VideoSerializer
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.core.exceptions import ObjectDoesNotExist


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
        if video_id:
            video = Video.objects.filter(id=video_id)\
                .prefetch_related('comments')\
                .select_related('related_profile').first()

            video_serialized = VideoSerializer(video)
            profile_serialized = LightProfileSerializer(video.related_profile)
            comments_serialized = CommentSerializer(video.comments, many=True)

            # TODO: Profile this query - gonna be gnarly

            to_return = video_serialized.data
            to_return['uploaded_by'] = profile_serialized.data
            to_return['comments'] = comments_serialized.data

            return Response(status=200, data=to_return)
        return Response(status=404)

    def list(self, request, *args, **kwargs):
        # queryset = Video.objects.order_by('-rank_total').select_related('related_profile')[:25]
        # serialized = VideoSerializer(queryset, many=True)
        # return Response(serialized.data)
        return Response(status=501)

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

    @detail_route(methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope])
    def top(self, request, pk=None):
        queryset = Video.objects.order_by('-rank_total').select_related('related_profile')[:25]
        serialized = VideoSerializer(queryset, many=True)
        return Response(serialized.data)

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
                rank_amount = request.data.get('rank_amount', 1)

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
        video.title = request_data.get('title', video.title)
        video.hashtag = request_data.get('hashtag', video.hashtag)
        category = request_data.get('category', False)

        if category:
            new_category = Category.objects.get(id=category)
            video.category = new_category

        video.save()