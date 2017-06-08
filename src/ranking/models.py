from django.db import models
from src.Ranked.basemodels import Base
from src.profile.mixins import ProfileRelatable


class Ranking(Base, ProfileRelatable):
    video = models.ForeignKey('video.Video')
    # Picture here ... can be either or ... maybe

    def remove_ranking(self):
        # Re-Process the ranking count on the associated item.
        # OnDelete
        pass