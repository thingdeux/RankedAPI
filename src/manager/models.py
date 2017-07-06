from django.db import models
from src.Ranked.basemodels import Base
from django.utils import timezone
from datetime import timedelta


class EnvironmentState(Base):
     last_updated_ranking_scores = models.DateTimeField(auto_now_add=True)
     is_updating_ranking = models.BooleanField(default=False)
     is_in_maintenance_mode = models.BooleanField(default=False)

     @staticmethod
     def get_environment_state():
         # Should only be one environment state - all accessors should access state this way.
         return EnvironmentState.objects.get_or_create(id=1)[0]

     @property
     def should_update_ranking(self):
         if not self.is_in_maintenance_mode and not self.is_updating_ranking:
             if timezone.now() > self.last_updated_ranking_scores + timedelta(minutes=30):
                 return True
         return False