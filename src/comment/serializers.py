from .models import Comment
from src.profile.serializers import LightProfileSerializer
from rest_framework import permissions, viewsets,serializers

class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    posted_date = serializers.DateField()
    posted_by = serializers.SerializerMethodField()

    def get_posted_by(self, transaction):
        return LightProfileSerializer(transaction.related_profile).data

    class Meta:
        fields = ['text', 'posted_date', 'related_profile']
        read_only_fields = ('text', 'posted_date', 'related_profile')
        model = Comment
