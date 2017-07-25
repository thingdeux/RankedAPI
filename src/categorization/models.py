from django.db import models
from src.Ranked.basemodels import Base, Hashtagable, ThumbnailDisplayable, Activatable, Orderable
from .mixins import ParentCategoryRelatable


class Category(Base, Hashtagable, ThumbnailDisplayable, Activatable, ParentCategoryRelatable, Orderable):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        try:
            return "({})-{}".format(self.parent_category.name, self.name)
        except AttributeError:
            return self.name