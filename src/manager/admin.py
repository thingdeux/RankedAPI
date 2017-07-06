from django.contrib import admin
from .models import EnvironmentState

class StateAdmin(admin.ModelAdmin):
    fields = ('is_updating_ranking', 'last_updated_ranking_scores', 'is_in_maintenance_mode')
    readonly_fields = ('is_updating_ranking','last_updated_ranking_scores')

admin.site.register(EnvironmentState, StateAdmin)
