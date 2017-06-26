from rest_framework import permissions, viewsets,serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'username', 'email', 'avatar_url', 'is_partner', 'is_featured', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id','is_partner', 'is_featured')
        model = Profile


class LightProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'avatar_url', 'username']
        read_only_fields = ('id', 'avatar_url', 'is_partner', 'is_featured', 'username')
        model = Profile