from django.db import models
from src.Ranked.basemodels import Base
from src.profile.mixins import ProfileRelatable


class Ranking(Base, ProfileRelatable):
    video = models.ForeignKey('video.Video', related_name="rankings", db_index=True)
    rank_amount = models.IntegerField(default=1)
    # Picture here ... can be either or ... maybe