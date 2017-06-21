from django.db import models

class VideoRelatable(models.Model):
    related_video = models.ForeignKey("video.Video", name="video")

    class Meta:
        abstract = True