from rest_framework import permissions, routers, serializers, viewsets
# Project Imports
from .models import Video

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'title', 'category', 'sub_category', 'is_featured',
                  'is_processing', 'ranking', 'hashtag', 'mobile',
                  'low', 'high', 'hd', 'is_active', 'thumbnail_large', 'thumbnail_small']

        read_only_fields = ('id', 'is_featured', 'is_processing', 'ranking', 'is_active', 'processing_progress',
                            'mobile', 'low', 'high', 'hd', 'thumbnail_large', 'thumbnail_small')
        model = Video