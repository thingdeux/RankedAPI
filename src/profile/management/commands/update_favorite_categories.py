# Django Imports
from django.core.management.base import LabelCommand
from django.db import transaction
from django.utils import timezone
# Standard Library Imports
import os
# Project Imports
from src.video.models import Video
from src.categorization.models import Category
from src.profile.models import Profile
from src.manager.models import EnvironmentState
import logging

logger = logging.getLogger("cron.update_categories")


class Command(LabelCommand):
    help = "Update Favorite Categories for all profiles"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.Ranked.settings")
        self.stdout.write("Updating Profile Fav. Categories!", ending='\n')
        logger.info("Updating Profile Fav. Categories!")

        _update_favorite_categories()
        logger.info("Done Updating Favorite Profiles!")


# HELPER FUNCTIONS
def _update_favorite_categories():
    """
    Update each profiles' favorite categories from their uploaded videos.
    """
    # TODO: Run as a celery job.
    state = EnvironmentState.get_environment_state()
    should_update = state.should_update_profiles_favorite_categories

    if not should_update:
        logger.info("No need to update favorite categories - bailing.")
        return

    state.is_updating_favorite_categories = True
    state.save()

    try:
        logger.info("Processing Profile Favorite Categories")

        with transaction.atomic():
            for profile in Profile.objects.filter(is_active=True):
                __update_favorite_category_for_profile(profile)
            state.last_updated_favorite_categories = timezone.now()
            state.is_updating_favorite_categories = False
            state.save()
    except Exception as error:
        logger.error("Error Running Profile Category Update Job {}".format(error))
        state.is_updating_favorite_categories = False
        state.save()


def __update_favorite_category_for_profile(profile):
    logger.info("Processing Favorite Category for Id: {}".format(profile.id))
    uploaded_videos_queryset = Video.get_videos_performant_queryset()
    uploaded_videos_queryset = uploaded_videos_queryset.filter(related_profile__id=profile.id)
    if uploaded_videos_queryset.count() > 0:
        category_counter = {}

        # Count uploaded videos categories then map into an array of tuples, sort, and take the top 2
        for video in uploaded_videos_queryset:
            if video.category:
                try:
                    category_counter[video.category] += 1
                except KeyError:
                    category_counter[video.category] = 1

        categories_converted_to_list = list(map(lambda item: (item[0], item[1]), category_counter.items()))
        favorite_two = sorted(categories_converted_to_list, key=lambda x: x[1], reverse=True)[:2]
        fav_two_count = len(favorite_two)

        if fav_two_count == 2:
            profile.primary_category = favorite_two[0][0]
            profile.secondary_category = favorite_two[1][0]
        elif fav_two_count == 1:
            profile.primary_category = favorite_two[0][0]
            profile.secondary_category = None
        else:
            profile.secondary_category = None
            profile.primary_category = None
        profile.save()
