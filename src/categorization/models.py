from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, ThumbnailDisplayable, Activatable
from .mixins import ParentCategoryRelatable


class Category(Base, Hashtagable, ThumbnailDisplayable, Activatable, ParentCategoryRelatable):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)

    def __str__(self):
        try:
            return "({})-{}".format(self.parent_category.name, self.name)
        except AttributeError:
            return self.name