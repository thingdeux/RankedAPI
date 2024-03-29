from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    search_fields = ('id', 'custom_field1')
    fields = ('title', 'hashtag', 'mobile', 'low', 'high', 'hd', 'thumbnail_small', 'thumbnail_large',
              'category', 's3_filename', 'is_processing', 'pre_signed_upload_url',
              'rank_total', 'is_top_10', 'is_active', 'is_featured', 'custom_field1')
    readonly_fields = ('s3_filename','is_processing', 'pre_signed_upload_url', 'is_top_10', 'custom_field1')

admin.site.register(Video, VideoAdmin)
