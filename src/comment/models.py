from django.db import models
# Project Imports
from src.Ranked.basemodels import Base
from src.profile.mixins import ProfileRelatable


class Comment(Base, ProfileRelatable):
    text = models.CharField(max_length=512)
    posted_date = models.DateField(auto_created=True)