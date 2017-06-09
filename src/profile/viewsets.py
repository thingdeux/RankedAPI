from rest_framework import permissions, routers, serializers, viewsets
from rest_framework.response import Response

from .models import Profile

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class ProfileSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Profile(**validated_data)

    class Meta:
        fields = ['id', 'email', 'avatar_url', 'is_partner', 'is_featured', 'phone_number', 'username']
        read_only_fields = ('is_partner', 'is_featured')
        model = Profile

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    """
    Viewset for User Registration
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Get e-mail post param
            # Make sure e-mail doesn't already exist
            serialized_profile = ProfileSerializer(data=request.data)
            if serialized_profile.is_valid():
                existing_account = list(Profile.objects.filter(email=serialized_profile.validated_data['email']))
                if len(existing_account) > 0:
                    error = {"description": "E-Mail already exists"}
                    return Response(status=408, data=error)

                new_profile = serialized_profile.save()
                new_profile.save()
                serialized_new_profile = ProfileSerializer(new_profile)
                return Response(status=201, data=serialized_new_profile.data)
            else:
                # TODO: If 'email' or 'username' is in the errors dict then 408 otherwise 400
                error = {"description": str(serialized_profile.errors) }
                return Response(status=400, data=error)
        except KeyError as e:
            error = {"description": "Not sending over proper values {}".format(e)}
            return Response(status=400)

