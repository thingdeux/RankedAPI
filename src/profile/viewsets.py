from rest_framework import permissions, routers, serializers, viewsets
from .models import Profile

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer