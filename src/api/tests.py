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

        response = self.client.get('/api/v1/search/?category=1', format='json')
        self.assertEqual(response.status_code, 200)




    def setUp(self):
        self.client = APIClient()

        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.test_profile2 = Profile(username="test_user2", password="testpass", email="test2@user.com")
        self.test_profile2.save()
        self.__create_auth_tokens()

        self.video1 = Video(related_profile=self.test_profile, title="My Video", is_processing=False, is_active=True)
        self.video1.save()
        self.video2 = Video(related_profile=self.test_profile2, title="My Video", is_processing=False, is_active=True)
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