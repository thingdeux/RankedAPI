# Standard Library Imports
import csv
import os
import uuid
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

    def create_update_profiles(self):
        self.__create_or_update_accounts()
        self.__update_followed_profiles()

    def create_update_videos(self):
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
        self.django_profiles = {
            username: self.__add_or_update_profile_if_needed(profile) for username, profile in self.profiles.items()
        }

    @transaction.atomic()
    def __create_or_update_videos(self):
        for profile in self.django_profiles:
            try:
                imported_profile = self.profiles[profile.username]
                _ = [self.__add_or_update_video(video, profile) for video in imported_profile.videos]
            except KeyError:
                raise("Error finding profile {}".format(profile.username))

    # Video Specific Helpers
    def __add_or_update_video(self, imported_video: ImportedVideo, profile: Profile):
        video = None
        try:
            video = Video.objects.get(custom_field1=imported_video.s3filename, related_profile=profile)
        except ObjectDoesNotExist:
            video = Video.objects.create(custom_field1=imported_video.s3filename, related_profile=profile)
        finally:
            video.custom_field1 = imported_video.s3filename
            video.is_featured = imported_video.is_featured
            video.rank_total = imported_video.total_rank_amount
            video.hashtag = '#{}'.format(',#'.join(imported_video.hashtag_string_array))
            self.__add_category_to_video(imported_video.category_string, video)
            self.__generate_demo_urls(video, imported_video.s3filename)

            # TODO: Set this to True when Taylor is done uploading the videos
            video.is_active = False
            video.is_processing = False
            video.save()


        return video

    def __generate_demo_urls(self, video: Video, filename):
        # TODO: Should pull this from django settings.
        STATIC_URL = "http://static.goranked.com"
        video.high = 'http://{}/{}'.format("videos.goranked.com", filename)
        video.low = 'http://{}/{}.webm'.format("videos.goranked.com", filename.split('.')[0])
        filename_parsed = filename.split('.')[0]
        video.thumbnail_large = "{}/{}-00001.png".format(STATIC_URL, filename_parsed)
        video.thumbnail_small = "{}/{}-00002.png".format(STATIC_URL, filename_parsed)

    def __add_category_to_video(self, category_string, video):
        # Make successive category acquisition faster by storing results in a local dictionary.
        category = None
        try:
            category = self.categories[category_string]
        except KeyError:
            try:
                self.categories[category_string] = Category.objects.get(name=category_string)
                category = self.categories[category_string]
            except ObjectDoesNotExist:
                print("MISSING CATEGORY {}".format(category_string))
                raise
        finally:
            video.category = category

    # Profile Specific Helpers
    def __add_or_update_profile_if_needed(self, profile_to_update: Profile):
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

    @transaction.atomic()
    def __update_followed_profiles(self):
        for username, profile in self.django_profiles.items():
            imported_profile = self.profiles[username]
            for profile_string in imported_profile.following_string_array:
                profile.followed_profiles.add(self.django_profiles[profile_string])
            profile.save()

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
    importer.create_update_profiles()