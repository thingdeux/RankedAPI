from django.db import models
from django.contrib.auth.models import AbstractUser
# Project Imports
from src.Ranked.basemodels import Base

class Profile(AbstractUser, Base):
    email = models.EmailField(max_length=256, db_index=True)
    avatar_url = models.URLField(max_length=512, default=None, null=True)
    is_partner = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    last_logged_in = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=25, default=None, null=True)
    following_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    ranked_ten_count = models.IntegerField(default=0)

    primary_category = models.ForeignKey('categorization.Category', related_name='fav_category', null=True, db_index=True)
    secondary_category = models.ForeignKey('categorization.Category', related_name='second_fav_category',
                                           null=True, db_index=True)

    followed_profiles = models.ManyToManyField("profile.Profile")


    def follow_user(self, user_id):
        # Can't follow yourself
        if int(user_id) != self.id:
            profile_to_follow = Profile.objects.get(id=user_id)
            self.followed_profiles.add(profile_to_follow)

    def stop_following_user(self, user_id):
        profile_to_stop_following = Profile.objects.get(id=user_id)
        self.followed_profiles.remove(profile_to_stop_following)