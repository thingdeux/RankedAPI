# DRF Imports
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import detail_route
# Project Imports
from src.comment.serializers import CommentSerializer
from .models import Video
from src.ranking.models import Ranking
from src.profile.models import Profile

from src.profile.serializers import ProfileSerializer
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
                .select_related('related_profile')[0]

            video_serialized = VideoSerializer(video)
            profile_serialized = ProfileSerializer(video.related_profile)
            comments_serialized = CommentSerializer(video.comments, many=True)

            # TODO: Profile this query - gonna be gnarly

            to_return = video_serialized.data
            to_return['uploaded_by'] = profile_serialized.data
            to_return['comments'] = comments_serialized.data

            return Response(status=200, data=to_return)
        return Response(status=404)

    def list(self, request, *args, **kwargs):
        queryset = Video.objects.order_by('ranking')[:25]
        serialized = VideoSerializer(queryset, many=True)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        error = {"Description":  "POST to /videos/ is not how videos are created. Please see documentation."}
        return Response(status=505, data=error)

    @detail_route(methods=['post', 'delete'], permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope])
    def rank(self, request, pk=None):
        """
        Handle Video Ranking
        POST: Rank a video on a scale between 1-10
        DELETE: Remove Ranking for authorized user
        """
        try:
            video = Video.objects.get(id=pk)
            profile = self.request.user

            rank_amount = request.data.get('rank_amount', 1)
            if rank_amount > 10:
                rank_amount = 10

            new_rank, was_created = Ranking.objects.get_or_create(related_profile=profile, video=video, rank_amount=rank_amount)
            if was_created:
                new_rank.save()
                return Response(status=200)
            else:
                return Response(status=304)
        except ObjectDoesNotExist:
            error = {"Description": "Video Not Found"}
            return Response(status=404, data=error)