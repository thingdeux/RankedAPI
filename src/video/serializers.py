from rest_framework import serializers
# Project Imports
from .models import Video
from src.categorization.serializers import CategorySerializer
from src.profile.serializers import LightProfileSerializer

class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    rank_total = serializers.IntegerField(read_only=True)
    is_featured = serializers.BooleanField(read_only=True)
    is_processing = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    category = serializers.SerializerMethodField()

    hashtag = serializers.SerializerMethodField()
    image_links = serializers.SerializerMethodField()
    video_urls = serializers.SerializerMethodField()
    uploaded_by = serializers.SerializerMethodField(read_only=True)

    def get_hashtag(self, model):
        if model.hashtag:
            return model.hashtag.split(',')
        return None

    def get_uploaded_by(self, model):
        return LightProfileSerializer(model.related_profile).data

    def get_category(self, model):
        if model.category:
            return CategorySerializer(model.category).data
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
                  'low', 'high', 'hd', 'is_active', 'thumbnail_large', 'thumbnail_small', 'top_10_ranking']

        read_only_fields = ('id', 'is_featured', 'is_processing', 'rank_total', 'is_active', 'processing_progress',
                            'mobile', 'low', 'high', 'hd', 'thumbnail_large', 'thumbnail_small', 'top_10_ranking')
        model = Video


class SearchVideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    rank_total = serializers.IntegerField(read_only=True)
    hashtag = serializers.SerializerMethodField()
    is_featured = serializers.BooleanField()
    image_links = serializers.SerializerMethodField()
    video_urls = serializers.SerializerMethodField()
    result_type = serializers.SerializerMethodField()

    def get_hashtag(self, model):
        if model.hashtag:
            return model.hashtag.split(',')
        return None


    def get_result_type(self, model):
        return "Video"

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
        fields = ['id', 'title', 'is_featured', 'rank_total', 'hashtag', 'mobile',
                  'low', 'high', 'hd', 'is_active', 'thumbnail_large', 'thumbnail_small']

        read_only_fields = ('id', 'is_featured', 'is_processing', 'rank_total', 'is_active', 'processing_progress',
                            'mobile', 'low', 'high', 'hd', 'thumbnail_large', 'thumbnail_small')
        model = Video