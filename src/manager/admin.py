from django.contrib import admin
from .models import EnvironmentState

class StateAdmin(admin.ModelAdmin):
    readonly_fields = ('is_updating_ranking',)

admin.site.register(EnvironmentState, StateAdmin)
