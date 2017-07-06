# Django Imports
from django.core.management.base import LabelCommand
from django.db import transaction
from django.utils import timezone
# Standard Library Imports
import os
# Project Imports
from src.video.models import Video
from src.categorization.models import Category
from src.manager.models import EnvironmentState
import logging

logger = logging.getLogger("cron.update_ranking")


class Command(LabelCommand):
    help = "Update Top_10 rankings for each Category"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.Ranked.settings")
        self.stdout.write("Updating Video Rankings!", ending='\n')
        logger.info("Updating Video Rankings!")

        _update_top_ten_rankings()
        logger.info("Done Updating Video Rankings!")


# HELPER FUNCTIONS
def _update_top_ten_rankings():
    """
    Update the ranking for videos in each category. To be run as a cron (or celery) job.

    Performance:
        3 Queries per Category
        Worst case 0(n + 4 + 10) where n == Categories
    """
    state = EnvironmentState.get_environment_state()

    if not state.should_update_ranking:
        return

    state.is_updating_ranking = True
    state.save()

    try:
        logger.info("Processing Video Ranking Updates")

        with transaction.atomic():
            for category in Category.objects.filter(is_active=True):
                logger.info("Processing Video Ranking for {}".format(category.name))

                top_10_videos_for_category = Video.objects.filter(category__id=category.id,
                                                                  is_active=True).order_by('-rank_total').values_list()[:10]

                top_10_ids = [x[0] for x in top_10_videos_for_category]

                # Kill previous top 10 rankings
                Video.objects.filter(is_top_10=True, category__id=category.id)\
                    .update(is_top_10=False, top_10_ranking=None)

                Video.objects.filter(id__in=top_10_ids).update(is_top_10=True)

                updated_videos = Video.objects.filter(is_top_10=True, category__id=category.id).order_by('-rank_total')
                for i, video in enumerate(updated_videos):
                    video.top_10_ranking = i + 1
                    video.save()

            state.is_updating_ranking = False
            state.last_updated_ranking_scores = timezone.now()
            state.save()
    except Exception as error:
        logger.error("Error Running Ranking Update Job {}".format(error))
        state.is_updating_ranking = False
        state.save()
