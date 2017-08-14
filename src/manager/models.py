from django.db import models
from src.Ranked.basemodels import Base
from django.utils import timezone
from datetime import timedelta


class EnvironmentState(Base):
     last_updated_ranking_scores = models.DateTimeField(auto_now_add=True)
     last_updated_favorite_categories = models.DateTimeField(default=timezone.now)

     is_updating_ranking = models.BooleanField(default=False)
     is_in_maintenance_mode = models.BooleanField(default=False)
     is_updating_favorite_categories = models.BooleanField(default=False)

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

     @property
     def should_update_profiles_favorite_categories(self):
         should_force_update = (timezone.now() - self.last_updated_favorite_categories).days > 0
         if should_force_update:
             return True

         if not self.is_in_maintenance_mode and not self.is_updating_favorite_categories:
             if timezone.now() > self.last_updated_favorite_categories + timedelta(minutes=60):
                 return True
         return False