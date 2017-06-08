from django.db import models
from django.contrib.auth.models import AbstractUser
# Project Imports
from src.Ranked.basemodels import Base

class Profile(AbstractUser, Base):
    email = models.EmailField(max_length=256)
    avatar_url = models.URLField(max_length=512)
    is_partner = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    last_logged_in = models.DateField(auto_now_add=True)