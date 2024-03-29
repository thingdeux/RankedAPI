# DRF Imports
from rest_framework.test import APIClient
# 3rd Party Imports
from oauthlib.common import generate_token
# Django Imports
from django.test import TestCase
from django.utils import timezone
# Project Imports
from src.video.models import Video
from src.profile.models import Profile
from src.ranking.models import Ranking
from src.comment.models import Comment
from src.categorization.models import Category
from oauth2_provider.models import Application, AccessToken
# Standard Library Imports
from datetime import timedelta

class SearchExploreAPICase(TestCase):

    def test_search_explore_success(self):
        """
        Account creation success
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/search/?category={}'.format(self.category.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 1)
        self.assertEqual(response.data['videos'][0]['title'], "My Video")

    def test_search_explore_limit_query(self):
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        for i in range(0, 20):
            video = Video(related_profile=self.test_profile, title="My Video", is_processing=False,
                                is_active=True,
                                hashtag="#love,#beats,", category=self.category)
            video.save()

        response = self.client.get('/api/v1/search/?category={}'.format(self.category.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 21)

        response = self.client.get('/api/v1/search/?category={}&limit=5'.format(self.category.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 5)

    def test_search_explore_offset_query(self):
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/search/?category={}'.format(self.category.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 1)

        response = self.client.get('/api/v1/search/?category={}&offset=1'.format(self.category.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 0)

    def test_search_trendsetters_success_less_than_20(self):
        """
        If not enough accounts exist for 20 random ids - just return what we have.
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/search/trendsetters/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['profiles']), 2)

    def test_search_hashtag_success(self):
        """
        You should be able to search for videos by hashtag
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/search/explore/?name=beats', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 2)

        response = self.client.get('/api/v1/search/explore/?name=love', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 1)

    def test_search_hashtag_case_insensitive_success(self):
        """
        You should be able to search for videos by hashtag
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/search/explore/?name=loveontherocks', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['videos']), 1)

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(name="Tarts")
        self.category.save()
        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.test_profile2 = Profile(username="test_user2", password="testpass", email="test2@user.com")
        self.test_profile2.save()
        self.__create_auth_tokens()

        self.video1 = Video(related_profile=self.test_profile, title="My Video", is_processing=False, is_active=True,
                            hashtag="#love,#beats,", category=self.category)
        self.video1.save()
        self.video2 = Video(related_profile=self.test_profile2, title="My Video2", is_processing=False, is_active=True,
                            hashtag="#beats,#loveOnTheRocks,", category=None)
        self.video2.save()

    def __create_auth_tokens(self):
        self.application = Application.objects.create(
            client_type='Resource owner password-based',
            authorization_grant_type=Application.CLIENT_PUBLIC,
            client_secret='121212',
            client_id='123123123',
            redirect_uris='',
            name='testAuth',
            user=self.test_profile
        )
        self.application.save()

        self.test_profile_token = AccessToken.objects.create(
            user=self.test_profile,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=600),
            token=generate_token(),
            application=self.application
        )
        self.test_profile_token.save()

        self.test_profile2_token = AccessToken.objects.create(
            user=self.test_profile2,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=600),
            token=generate_token(),
            application=self.application
        )
        self.test_profile2.save()