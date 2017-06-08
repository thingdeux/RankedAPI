from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, MultipleQualityLinkable, ThumbnailDisplayable, UploadProcessable
from src.profile.mixins import ProfileRelatable


class Category(Base, Hashtagable):
    """
    Category and sub-category for videos / pics... etc

    A Sub-Category will be stored on the same table but will have a parent_category relationship.
    """

    name = models.CharField(max_length=256, null=False, blank=False)
    # Any Category can have a subcategory
    parent_category = models.ForeignKey('self', default=None, related_name='parent')


class Video(Base, Hashtagable, ProfileRelatable, MultipleQualityLinkable, ThumbnailDisplayable, UploadProcessable):
    title = models.CharField(max_length=256, blank=False, null=False)
    ranking = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_processing = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=False)
    sub_category = models.ForeignKey(Category, related_name='sub_category')