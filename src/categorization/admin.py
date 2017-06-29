from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'hashtag', 'thumbnail_large', 'thumbnail_small', 'parent_category', 'is_active')

admin.site.register(Category, CategoryAdmin)
