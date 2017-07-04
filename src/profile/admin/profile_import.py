# Standard Library Imports
import csv
import os
# Project Imports
from src.categorization.models import Category
from src.profile.models import Profile
from src.video.models import Video
# Django Imports
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


BASE_DIR = os.path.dirname(__file__)

class ImportedProfile:
    def __init__(self, row_data):
        self.username = row_data[0]
        self.password = row_data[1]
        self.favorite_category1 = row_data[2]
        self.favorite_category2 = row_data[3]
        self.avatar_url = row_data[5]
        self.is_featured = row_data[6] == "YES"
        self.is_partner = row_data[7] == "YES"
        self.following_string_array = str(row_data[8]).replace(' ', '').split(',')

    def __str__(self):
        return str("{}: {}".format(self.username, self.following_string_array))

    def add_video(self, video):
        try:
            self.videos.append(video)
        except AttributeError:
            self.videos = []
            self.videos.append(video)

class ImportedVideo:
    def __init__(self, row_data):
        self.associated_username = row_data[0]
        self.s3filename = row_data[1]
        self.title = row_data[3]
        self.hashtag_string_array = str(row_data[4]).replace(' ', '').split(',')
        self.category_string = row_data[5]
        self.is_featured = row_data[6] == "YES"
        self.total_rank_amount = int(row_data[7])

class ProfileImporter:
    def __init__(self):
        self.categories = {}
        # Profiles is a Dictionary of ImportedProfile objects keyed on username for easier access during video import.
        self.profiles = self.__get_profiles_from_csv()
        self.__add_videos_from_csv()

    def run(self):
        self.__create_or_update_accounts()
        self.__create_or_update_videos()

    # CSV Interactions
    def __get_profiles_from_csv(self):
        dict_to_return = {}

        with open(os.path.join(os.path.dirname(__file__), "Profile Import Sheet - Profile.csv"), 'r') as file:

            reader = csv.reader(file)
            for row_num, row in enumerate(reader):
                # Skip the first row, Header Row
                if row_num == 0:
                    continue
                profile = ImportedProfile(row)
                dict_to_return[profile.username] = profile

        return dict_to_return

    def __add_videos_from_csv(self):
        with open(os.path.join(os.path.dirname(__file__), "Profile Import Sheet - Videos.csv"), 'r') as file:

            reader = csv.reader(file)
            for row_num, row in enumerate(reader):
                # Skip the first row, Header Row
                if row_num == 0:
                    continue
                video = ImportedVideo(row)
                self.profiles[video.associated_username].add_video(video)

    # Django Interactions
    @transaction.atomic()
    def __create_or_update_accounts(self):
        # Speed up the creation process and limit the number of queries using atomic transaction.
        self.django_profiles = [self.__add_or_update_profile_if_needed(profile) for profile in self.profiles.values()]

    @transaction.atomic()
    def __create_or_update_videos(self):
        pass

    def __add_or_update_profile_if_needed(self, profile_to_update):
        profile = None
        try:
            profile = Profile.objects.get(username=profile_to_update.username)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(username=profile_to_update.username)
        finally:
            profile.avatar_url = profile_to_update.avatar_url
            profile.set_password(profile_to_update.password)
            self.__add_category_to_profile(profile_to_update.favorite_category1, profile)
            self.__add_category_to_profile(profile_to_update.favorite_category2, profile, False)
            profile.is_active = True
            profile.is_partner = profile_to_update.is_partner
            profile.is_featured = profile_to_update.is_featured
            profile.save()

        return profile

    def __add_category_to_profile(self, category_string, profile, is_primary=True):
        # Make successive category acquisition faster by storing results in a local dictionary.
        category = None
        try:
            category = self.categories[category_string]
        except KeyError:
            try:
                self.categories[category_string] = Category.objects.get(name=category_string)
                category = self.categories[category_string]
            except ObjectDoesNotExist:
                raise("MISSING CATEGORY {}".format(category_string))
        finally:
            if is_primary:
                profile.primary_category = category
            else:
                profile.secondary_category = category

if __name__ == "__main__":
    importer = ProfileImporter()
    importer.run()