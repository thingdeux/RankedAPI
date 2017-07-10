from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, MultipleQualityLinkable, ThumbnailDisplayable, UploadProcessable
from src.Ranked.basemodels import Activatable, Rankable, CustomFieldStorable
from src.profile.mixins import ProfileRelatable
from src.categorization.mixins import MultiCategoryRelatable


class Video(Base, Hashtagable, ProfileRelatable, MultipleQualityLinkable, CustomFieldStorable,
            ThumbnailDisplayable, UploadProcessable, Activatable, Rankable, MultiCategoryRelatable):

    title = models.CharField(default="", max_length=256, blank=False, null=False)
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return "{}'s video {}".format(self.related_profile, self.id)

    @staticmethod
    def get_ranked_10_videos_queryset(category=None, title_filter=None):
        """
        Get videos queryset for videos that have is_ranked_10 flag set.

        :param title_filter: Filter results by title
        :return: Queryset
        """
        base_queryset = Video.objects.order_by('-rank_total')\
            .filter(is_top_10=True, is_active=True)\
            .select_related('related_profile').select_related('category').select_related('category__parent_category')

        if category:
            base_queryset = base_queryset.filter(category__id=category)

        if title_filter:
            base_queryset = base_queryset.filter(title__icontains=title_filter.lower())[:50]

        return base_queryset

    @staticmethod
    def get_ranked_trending_videos_queryset():
        """
        Get videos queryset for highest ranked videos (for now) - will need to determine what 'trending' means later.

        :return: Queryset
        """
        base_queryset = Video.objects.order_by('-rank_total')\
            .filter(is_active=True)\
            .select_related('related_profile').select_related('category')[:50]

        return base_queryset