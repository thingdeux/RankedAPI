from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from src.profile.models import Profile

class ProfileAdmin(UserAdmin):
    search_fields = ('username',)
    readonly_fields = ('last_logged_in', 'is_partner', 'is_featured')
    fieldsets = UserAdmin.fieldsets + (
        ("Ranked Properties", {'fields': ('avatar_url', 'is_partner', 'is_featured', 'last_logged_in', 'following_count',
                     'followers_count', 'ranked_ten_count')}),
    )
admin.site.register(Profile, ProfileAdmin)