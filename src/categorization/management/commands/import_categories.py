# Django Imports
from django.core.management.base import LabelCommand
# Standard Library Imports
import os
# Project Imports
from src.categorization.admin import csv_import


class Command(LabelCommand):
    help = "Manually import or delete categories"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.Ranked.settings")
        try:
            self.stdout.write("Importing / Updating Categories", ending='\n')
            csv_import.import_categories(should_overwrite=False)
        except IndexError:
            self.stdout.write("No command provided, available options: 'import' / 'wipe'", ending='\n')
