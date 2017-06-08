from django.db import models

class ProfileRelatable(models.Model):
    related_profile = models.ForeignKey("profile.Profile")

    class Meta:
        abstract = True