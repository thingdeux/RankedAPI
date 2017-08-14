from django.contrib import admin
from .models import EnvironmentState

class StateAdmin(admin.ModelAdmin):
    fields = ('last_updated_favorite_categories', 'last_updated_ranking_scores', 'is_updating_ranking',
              'is_updating_favorite_categories', 'is_in_maintenance_mode')
    readonly_fields = ('last_updated_ranking_scores',)

admin.site.register(EnvironmentState, StateAdmin)
