from django.db import models
from django.contrib.auth.models import AbstractUser
# Project Imports
from src.Ranked.basemodels import Base
from src.categorization.models import Category
from src.categorization.serializers import CategorySerializer

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

    @property
    def favorite_category(self):
        if self.primary_category:
            return CategorySerializer(self.primary_category).data
        else:
            return None

    @property
    def second_favorite_category(self):
        if self.secondary_category:
            return CategorySerializer(self.secondary_category).data
        else:
            return None

    @property
    def user_ids_i_follow(self):
        return self.followed_profiles.values('id').prefetch_related('followed_profiles')

    def follow_user(self, user_id):
        # Can't follow yourself
        if int(user_id) != self.id:
            profile_to_follow = Profile.objects.get(id=user_id)

            self.followed_profiles.add(profile_to_follow)
            self.following_count = self.followed_profiles.count()

            profile_to_follow.followers_count = Profile.objects.filter(followed_profiles__id=profile_to_follow.id).count()
            profile_to_follow.save()


    def stop_following_user(self, user_id):
        profile_to_stop_following = Profile.objects.get(id=user_id)
        self.followed_profiles.remove(profile_to_stop_following)

    @staticmethod
    def get_trend_setters_queryset():
        """
        Get videos queryset for videos that have is_ranked_10 flag set.

        """
        # TODO: Make this work - is mocked for demo
        # TODO: Choose some useful profiles or heck, just randomize
        return Profile.objects.filter(id__in=[1,3,55], is_active=True)\
            .select_related('primary_category').select_related('secondary_category')\
            .prefetch_related('followed_profiles')\
            .select_related('followed_profiles__primary_category')\
            .select_related('followed_profiles__secondary_category')