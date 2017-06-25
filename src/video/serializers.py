from rest_framework import permissions, routers, serializers, viewsets
# Project Imports
from .models import Video
from src.categorization.serializers import CategorySerializer

class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    rank_total = serializers.IntegerField()
    is_featured = serializers.BooleanField()
    is_processing = serializers.BooleanField()
    is_active = serializers.BooleanField()

    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    hashtag = serializers.CharField()
    image_links = serializers.SerializerMethodField()
    video_urls = serializers.SerializerMethodField()

    def get_category(self, model):
        if model.category:
            return CategorySerializer(model.category).data
        return None

    def get_sub_category(self, model):
        if model.category:
            return CategorySerializer(model.sub_category).data
        return None

    def get_video_urls(self, model):
        return {
            'mobile': model.mobile,
            'low': model.low,
            'high': model.high,
            'hd': model.hd
        }

    def get_image_links(self, model):
        return {
            'thumbnail': model.thumbnail_small,
            'large': model.thumbnail_large
        }

    class Meta:
        fields = ['id', 'title', 'category', 'sub_category', 'is_featured',
                  'is_processing', 'rank_total', 'hashtag', 'mobile',
                  'low', 'high', 'hd', 'is_active', 'thumbnail_large', 'thumbnail_small']

        read_only_fields = ('id', 'is_featured', 'is_processing', 'rank_total', 'is_active', 'processing_progress',
                            'mobile', 'low', 'high', 'hd', 'thumbnail_large', 'thumbnail_small')
        model = Video