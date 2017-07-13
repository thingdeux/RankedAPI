from django.db import models
from src.Ranked.basemodels import Base
from src.profile.mixins import ProfileRelatable


class Ranking(Base, ProfileRelatable):
    video = models.OneToOneField('video.Video', related_name="rankings", db_index=True)
    rank_amount = models.IntegerField(default=1)
    # Picture here ... can be either or ... maybe

    def remove_ranking(self):
        # Re-Process the ranking count on the associated item.
        # OnDelete
        pass

    def add_ranking(self):
        # Re-Process the ranking count on the associated video (or pic)
        pass

    