from rest_framework import permissions, viewsets,serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        new_profile = Profile.objects.create(**validated_data)
        if validated_data.get('password', False):
            new_profile.set_password(validated_data['password'])
        return new_profile


    def update(self, instance, validated_data):
        """
        Update and return profile instance
        """
        # Can't update your username
        instance.email = validated_data.get('email', instance.email)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        if validated_data.get('password', False):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


    class Meta:
        fields = ['id', 'username', 'email', 'avatar_url', 'is_partner', 'is_featured', 'phone_number', 'password',
                  'following_count', 'followers_count', 'ranked_ten_count']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id','is_partner', 'is_featured', 'following_count', 'followers_count', 'ranked_ten_count')
        model = Profile


class LightProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'avatar_url', 'username', 'is_partner', 'is_featured']
        read_only_fields = ('id', 'avatar_url', 'is_partner', 'is_featured', 'username')
        model = Profile