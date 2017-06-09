from rest_framework import permissions, routers, serializers, viewsets
from rest_framework.response import Response

from .models import Profile

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer








class Registration():
    def __init__(self, email, username, password, unlock_key, phone_number):
        self.email = email
        self.username = username
        self.password = password
        self.unlock_key = unlock_key
        self.phone_number = phone_number


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=4)
    username = serializers.CharField(min_length=2, max_length=40)
    password = serializers.CharField(min_length=4, max_length=100)
    unlock_key = serializers.CharField(min_length=8, max_length=8)
    phone_number = serializers.CharField()

    def create(self, validated_data):
        return Registration(**validated_data)



class RegisterViewSet(viewsets.ModelViewSet):
    """
    Viewset for User Registration
    """
    queryset = Profile.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Get e-mail post param
            # Make sure e-mai doesn't already exist
            serialized_profile = ProfileSerializer(data=request.data)
            if serialized_profile.is_valid():
                existing_account = list(Profile.objects.filter(email=serialized_profile.email))
                if len(existing_account) > 0:
                    return Response(status=408)

                return Response(serialized_profile.data)
            else:
                return Response(status=400)
        except KeyError:
            pass
