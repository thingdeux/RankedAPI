from django.db import models
from .exceptions import ParentCategoryMissingError, SubCategorySameAsParentError

class ParentCategoryRelatable(models.Model):
    parent_category = models.OneToOneField("categorization.Category", null=True, default=None)

    class Meta:
        abstract = True


class SubCategoryRelatable(models.Model):
    sub_category = models.OneToOneField("categorization.Category", related_name="sub_category", null=True, default=None)

    class Meta:
        abstract = True


class MultiCategoryRelatable(models.Model):
    category = models.ForeignKey("categorization.Category", related_name='primary_category', null=True)
    sub_category = models.ForeignKey("categorization.Category", related_name='sub_category', null=True)

    def add_sub_category(self, category):
        try:
            if self.category == None:
                raise ParentCategoryMissingError("Can't add a sub-category without defining a primary category")
            elif category.id == self.category.id:
                raise SubCategorySameAsParentError("Can't add a sub-category that's the same as the primary")
            else:
                self.sub_category = category
        except AttributeError:
            raise ParentCategoryMissingError("Can't add a sub-category without defining a primary category")

    class Meta:
        abstract = True