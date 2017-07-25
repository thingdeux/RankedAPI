from django.db import models

class ProfileRelatable(models.Model):
    related_profile = models.ForeignKey("profile.Profile", db_index=True)

    class Meta:
        abstract = True