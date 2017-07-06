from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, MultipleQualityLinkable, ThumbnailDisplayable, UploadProcessable
from src.Ranked.basemodels import Activatable, Rankable, CustomFieldStorable
from src.profile.mixins import ProfileRelatable
from src.categorization.mixins import MultiCategoryRelatable


class Category(Base, Hashtagable):
    """
    Category and sub-category for videos / pics... etc

    A Sub-Category will be stored on the same table but will have a parent_category relationship.
    """

    name = models.CharField(max_length=256, null=False, blank=False)
    # Any Category can have a subcategory
    parent_category = models.ForeignKey('self', default=None, related_name='parent')


class Video(Base, Hashtagable, ProfileRelatable, MultipleQualityLinkable, CustomFieldStorable,
            ThumbnailDisplayable, UploadProcessable, Activatable, Rankable, MultiCategoryRelatable):

    title = models.CharField(default="", max_length=256, blank=False, null=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return "{}'s video {}".format(self.related_profile, self.id)

    @staticmethod
    def get_ranked_10_videos_queryset(title_filter: str):
        """
        Get videos queryset for videos that have is_ranked_10 flag set.

        :param title_filter: Filter results by title
        :return: Queryset
        """
        base_queryset = Video.objects.order_by('-rank_total')\
            .filter(is_ranked_10=True, is_active=True)\
            .select_related('related_profile').select_related('category')

        if title_filter:
            # Note - tablescan....yuck
            base_queryset.filter(title__icontains='{}'.format(title_filter.lower()))

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