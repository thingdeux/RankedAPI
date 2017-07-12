# DRF Imports
from rest_framework import permissions, viewsets
from .serializers import CategorySerializer
# Django Imports
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Project Imports
from .models import Category
# Library Imports
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    TWENTY_FOUR_HOURS_IN_SECONDS = 86400

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True).select_related('parent_category')

    # @silk_profile(name='Category List')
    # def list(self, request, *args, **kwargs):
    #     categories = Category.objects.filter(is_active=True).select_related('parent_category')
    #     return Response(status=200, data=CategorySerializer(categories, many=True).data)

    @method_decorator(cache_page(TWENTY_FOUR_HOURS_IN_SECONDS))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).dispatch(request, *args, **kwargs)