# Standard Library Imports
from math import floor
import random
from rest_framework import serializers
# Project Imports
from .models import Video
from src.categorization.serializers import CategorySerializer
from src.profile.serializers import BasicProfileSerializer

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
    is_top_10 = serializers.BooleanField(read_only=True)
    top_10_ranking = serializers.IntegerField(read_only=True)
    average_rank = serializers.SerializerMethodField()
    views = serializers.IntegerField(read_only=True)

    def get_average_rank(self, model):
        if model.top_10_ranking:
            # If the video is one of the top 10 ranked videos return 10.
            return 10
        elif model.rank_total > 0:
            # TODO: Should actually be a field and be updated with the ranking algorithm.
            # For now just a rando. number between 1 and 9
            return floor(random.randint(1, 9))
        else:
            return 0


    def get_hashtag(self, model):
        if model.hashtag:
            # Kill trailing comma on serialization.
            return model.hashtag.split(',')[:-1]
        return None

    def get_uploaded_by(self, model):
        return BasicProfileSerializer(model.related_profile).data

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
                  'is_processing', 'is_top_10', 'average_rank',
                  'top_10_ranking','rank_total', 'views', 'hashtag', 'mobile',
                  'low', 'high', 'hd', 'is_active', 'thumbnail_large', 'thumbnail_small']

        read_only_fields = ('id', 'is_featured', 'is_processing', 'rank_total', 'views', 'is_active', 'processing_progress',
                            'mobile', 'low', 'high', 'hd', 'thumbnail_large', 'thumbnail_small', 'is_top_10',
                            'average_rank', 'top_10_ranking')
        model = Video