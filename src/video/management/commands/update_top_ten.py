# Django Imports
from django.core.management.base import LabelCommand
from django.db import transaction
# Standard Library Imports
import os
# Project Imports
from src.video.models import Video
from src.categorization.models import Category


class Command(LabelCommand):
    help = "Manually import and update profiles/videos"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.Ranked.settings")
        try:
            self.stdout.write("Importing / Profiles and Videos", ending='\n')
            _update_top_ten_rankings()
        except IndexError:
            self.stdout.write("No command provided, available options: 'import' / 'wipe'", ending='\n')


# HELPER METHODS

def _update_top_ten_rankings():
    """
    Update the ranking for videos in each category. To be run as a cron (or celery) job.

    Performance:
        3 Queries per Category
        Worst case 0(n + 4 + 10) where n == Categories
    """
    with transaction.atomic():
        for category in Category.objects.filter(is_active=True):
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

