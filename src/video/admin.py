from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'hashtag', 'mobile', 'low', 'high', 'hd', 'thumbnail_small', 'thumbnail_large',
              'category', 's3_filename', 'is_processing', 'pre_signed_upload_url',
              'rank_total', 'is_top_10', 'is_active', 'is_featured')
    readonly_fields = ('s3_filename','is_processing', 'pre_signed_upload_url', 'is_top_10')

admin.site.register(Video, VideoAdmin)
