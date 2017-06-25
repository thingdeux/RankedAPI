from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, ThumbnailDisplayable, Activatable
from .mixins import ParentCategoryRelatable


class Category(Base, Hashtagable, ThumbnailDisplayable, Activatable, ParentCategoryRelatable):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)