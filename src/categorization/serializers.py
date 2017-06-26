from rest_framework import permissions, viewsets,serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    hashtag = serializers.CharField()
    banner = serializers.SerializerMethodField()
    is_active = serializers.BooleanField()
    is_sub_category = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField()

    def get_parent_category(self, model):
        if model.parent_category:
            return CategorySerializer(model.parent_category).data
        else:
            return None

    def get_is_sub_category(self, model):
        return model.parent_category != None

    def get_banner(self, model):
        return model.thumbnail_large or model.thumbnail_small

    class Meta:
        fields = ['id', 'name', 'hashtag', 'banner', 'is_active', 'parent_category', 'is_sub_category', 'parent_category']
        read_only_fields = ('id', 'name','hashtag', 'thumbnail_large', 'thumbnail_small', 'is_active', 'parent_category')
        model = Category