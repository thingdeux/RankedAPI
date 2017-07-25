from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from src.profile.models import Profile

admin.site.register(Profile, UserAdmin)