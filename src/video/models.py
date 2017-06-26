from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, MultipleQualityLinkable, ThumbnailDisplayable, UploadProcessable
from src.Ranked.basemodels import Activatable, Rankable
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


class Video(Base, Hashtagable, ProfileRelatable, MultipleQualityLinkable,
            ThumbnailDisplayable, UploadProcessable, Activatable, Rankable, MultiCategoryRelatable):

    title = models.CharField(default="", max_length=256, blank=False, null=False)
    is_featured = models.BooleanField(default=False)