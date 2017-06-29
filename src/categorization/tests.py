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
from .models import Category
from oauth2_provider.models import Application, AccessToken
# Standard Library Imports
from datetime import timedelta
from django.core.cache import cache


class CategoryAPICase(TestCase):

    def test_category_list_success(self):
        """
        Category list success
        """
        response = self.client.get('/api/v1/categories/', format='json')

        self.assertEqual(len(response.data), 3)

        primary_category = response.data[0]
        self.assertEqual(primary_category['name'], "Dance")
        self.assertEqual(primary_category['is_sub_category'], False)
        self.assertEqual(primary_category['parent_category'], None)

        sub_category = response.data[1]
        self.assertEqual(sub_category['name'], "Breakdance")
        self.assertEqual(sub_category['is_sub_category'], True)
        self.assertEqual(sub_category['parent_category']['id'], 1)

    def test_category_list_empty(self):
        """
        Category list success with empty array
        """
        all_categories = Category.objects.all()
        all_categories.delete()

        response = self.client.get('/api/v1/categories/', format='json')

        self.assertEqual(len(response.data), 0)

    def setUp(self):
        self.client = APIClient()

        # OAuth Management and setup
        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.__create_auth_tokens()
        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        # Create Test Categories
        self.category_dance = Category(name="Dance", is_active=True)
        self.category_dance.save()

        self.sub_category_breakdance = Category(name="Breakdance", is_active=True, parent_category=self.category_dance)
        self.sub_category_breakdance.save()
        self.sub_category_funky_chicken = Category(name="Funky Chicken", is_active=True, parent_category=self.category_dance)
        self.sub_category_funky_chicken.save()

        self.video1 = Video(related_profile=self.test_profile, title="My Video", is_processing=False, is_active=True)
        self.video1.save()


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