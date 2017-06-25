# DRF Imports
from rest_framework import permissions, viewsets
from .serializers import CategorySerializer
# Project Imports
from .models import Category
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)