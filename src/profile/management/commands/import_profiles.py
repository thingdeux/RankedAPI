# Django Imports
from django.core.management.base import LabelCommand
# Standard Library Imports
import os
# Project Imports
from src.profile.admin_commands.profile_import import ProfileImporter


class Command(LabelCommand):
    help = "Manually import and update profiles/videos"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.Ranked.settings")
        try:
            self.stdout.write("Importing / Profiles and Videos", ending='\n')
            profile_importer = ProfileImporter()
            profile_importer.create_update_profiles()
            profile_importer.create_update_videos()
        except IndexError:
            self.stdout.write("No command provided, available options: 'import' / 'wipe'", ending='\n')
