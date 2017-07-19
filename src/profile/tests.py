# DRF Imports
from rest_framework.test import APIClient
# Django Imports
from django.test import TestCase
# Project Imports
from .models import Profile
from src.video.models import Video
from src.categorization.models import Category
from src.Ranked.test import APITestBase
# Django Imports
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
# 3rd Party Imports
from oauthlib.common import generate_token
from oauth2_provider.models import Application, AccessToken
# Standard Imports
from datetime import timedelta


class RegistrationTestCase(TestCase):
    def test_successful_account_creation(self):
        """
        Account creation success
        """
        response = self.client.post('/api/v1/users/register/', {
            'username': 'ishouldwork',
            'password': 'mo3435re',
            'email': 'shouldwork@user.media',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': 2,
            'username': 'ishouldwork',
            'is_featured': False,
            'email': 'shouldwork@user.media',
            'phone_number': None,
            'is_partner': False,
            'avatar_url': None,
            'following_count': 0,
            'followers_count': 0,
            'ranked_ten_count': 0,
            'favorite_category': None,
            'second_favorite_category': None
        })
        new_account = Profile.objects.get(id=2)
        self.assertIsNot(new_account.password, None)
        self.assertIsNot(new_account.password, "")

    def test_registration_email_exists(self):
        """
        Email is unique - verify two exact emails can't exist.
        """
        response = self.client.post('/api/v1/users/register/', data={
            'username': 'test_use23232r',
            'password': 'mo3435re',
            'email': 'test@user.com',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 408)
        self.assertEqual(response.data, {'description': 'E-Mail already exists'})

    def test_registration_username_exists(self):
        """
        Usernames are unique - verify two exact usernames can't exist.
        """
        response = self.client.post('/api/v1/users/register/', {
            'username': 'test_user',
            'password': 'mo3435re',
            'email': 'myunique1231231email@email.com',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'description': 'Errors in fields', 'errors': ['username']})

    def test_registration_multiple_fields_missing(self):
        """
        Username is a required field for registration and needs to always be included.
        Should fail if password isn't included.
        """
        response = self.client.post('/api/v1/users/register/', {
            'email': 'myuni1queema2il@email.com',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"description": "Not sending over proper values 'password'"})


    def test_registration_username_missing(self):
        """
        Username is a required field for registration and needs to always be included.
        Should fail if password isn't included.
        """
        response = self.client.post('/api/v1/users/register/', {

            'email': 'myuni1queema2il@email.com',
            'password': 'IbetThisDoesntWork',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"description": "Not sending over proper values 'username'"})


    def test_registration_password_missing(self):
        """
        Password is a required field for registration and needs to always be included.
        Should fail if password isn't included.
        """
        response = self.client.post('/api/v1/users/register/', {
            'username': 'macoroaht3',
            'email': 'myuniqueema2il@email.com',
            'access_code': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"description": "Not sending over proper values 'password'"})

    def test_registration_password_not_long_enough(self):
        """
        The only password restriction is that a password has to be at least 6 characters minimum.  Make sure
        That anything less than that returns http 400
        """
        response = self.client.post('/api/v1/users/register/', {
            'username': 'macoroaht',
            'password': 'more',
            'email': 'myuniqueemail@email.com',
            'access_code': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, { "description": "Password does not meet standards. At least 6 characters.", "errors": ["password"]})

    def setUp(self):
        self.client = APIClient()
        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.__create_auth_tokens()

    # TODO: Create generic version of this for sharing.
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

class UsersMeTestCase(TestCase):
    def test_me_success(self):
        """
        Profile /me test
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/users/me/')

        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(response.data,
             {
                'me': {
                    'id': 2,
                    'email': 'test@user.com',
                    'avatar_url': None,
                    'is_partner': False,
                    'is_featured': False,
                    'phone_number': None,
                    'username': 'test_user',
                    'following_count': 0,
                    'followers_count': 0,
                    'ranked_ten_count': 0,
                    'favorite_category': {
                        'is_sub_category': False,
                        'is_active': True,
                        'hashtag': 'Blessed',
                        'name': 'Pizza',
                        'banner': None,
                        'parent_category': None,
                        'id': 1
                    },
                    'second_favorite_category': {
                        'is_sub_category': False,
                        'is_active': True,
                        'hashtag': 'Blessed',
                        'name': 'Chocolate',
                        'banner': None,
                        'parent_category': None,
                        'id': 2
                    },
                },
                'my_ranked_video_ids': [],
                'videos': []
              })



    def test_users_ranked_videos_success(self):
        """
        The /users/me/ endpoint should return an array of the users ranked videos.
        """
        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        primary_category = Category(name="Dance")
        primary_category.save()
        sub_category = Category(name="Breakdance", is_active=True, parent_category=primary_category)
        sub_category.save()

        video1 = Video(related_profile=self.test_profile, title="My Video", is_processing=False, is_active=True,
                            thumbnail_small="http://MyThumb.jpg", thumbnail_large="http://MyLargeThumb.jpg",
                            category=sub_category, rank_total=300)
        video1.save()
        video2 = Video(related_profile=self.test_profile2, title="My Video", is_processing=False, is_active=True,
                            category=primary_category)
        video2.save()
        video3 = Video(related_profile=self.test_profile2, title="My Video3", is_processing=False, is_active=True,
                            category=primary_category)
        video3.save()

        _ = self.client.post('/api/v1/videos/{}/rank/'.format(video1.id), data={'rank_amount': 10}, format='json')
        _ = self.client.post('/api/v1/videos/{}/rank/'.format(video2.id), data={'rank_amount': 5}, format='json')
        _ = self.client.post('/api/v1/videos/{}/rank/'.format(video3.id), data={'rank_amount': 1}, format='json')

        videos_response = self.client.get('/api/v1/users/me/', format='json')

        ranked_videos = videos_response.data['my_ranked_video_ids']
        self.assertEqual(len(ranked_videos), 3)
        self.assertEqual(ranked_videos, [1, 2, 3])

        _ = self.client.delete('/api/v1/videos/{}/rank/'.format(video3.id), format='json')
        videos_response = self.client.get('/api/v1/users/me/', format='json')
        ranked_videos = videos_response.data['my_ranked_video_ids']
        self.assertEqual(len(ranked_videos), 2)
        self.assertEqual(ranked_videos, [1, 2])

    def setUp(self):
        self.client = APIClient()

        self.test_category = Category(name="Pizza", is_active=True, hashtag="Blessed")
        self.test_category.save()
        self.test_category2 = Category(name="Chocolate", is_active=True, hashtag="Blessed")
        self.test_category2.save()
        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.primary_category = self.test_category
        self.test_profile.secondary_category = self.test_category2
        self.test_profile2 = Profile(username="test_user2", password="testpass", email="test2@user.com")
        self.test_profile2.primary_category = self.test_category

        self.test_profile2.save()
        self.test_profile.save()
        self.__create_auth_tokens()

    # TODO: Create generic version of this for sharing.
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

class UsersFollowersTestCase(TestCase):

    def test_profile_follow_success(self):
        """
        /Followers should allow one profile to follow another.
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/users/{}/following/'.format(self.test_profile2.id), format="json")
        profile = Profile.objects.get(id=self.test_profile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.followed_profiles.all().count(), 1)

    def test_profile_stop_following_success(self):
        """
        /Followers should allow one profile to stop following another.
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        profile = Profile.objects.get(id=self.test_profile.id)
        profile.follow_user(self.test_profile2.id)
        profile.save()

        response = self.client.delete('/api/v1/users/{}/following/'.format(self.test_profile2.id), format="json")

        profile = Profile.objects.get(id=self.test_profile.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.followed_profiles.all().count(), 0)

    def test_profile_list_following(self):
        """
        /Followers GET should return a list of users followed profiles
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        profile = Profile.objects.get(id=self.test_profile.id)
        profile.follow_user(self.test_profile2.id)
        profile.follow_user(self.test_profile3.id)
        profile.save()

        response = self.client.get('/api/v1/users/{}/following/'.format(self.test_profile.id), format="json")

        profile = Profile.objects.get(id=self.test_profile.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.followed_profiles.all().count(), 2)
        self.assertEqual(len(response.data['users']), 2)

        response = self.client.get('/api/v1/users/{}/following/'.format(self.test_profile2.id), format="json")
        profile = Profile.objects.get(id=self.test_profile2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.followed_profiles.all().count(), 0)
        self.assertEqual(len(response.data['users']), 0)

    def test_profile_list_following_empty(self):
        """
        /following GET should return an empty list of users followed profiles when there are no followers.
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/users/{}/following/'.format(self.test_profile.id), format="json")

        profile = Profile.objects.get(id=self.test_profile.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.followed_profiles.all().count(), 0)
        self.assertEqual(len(response.data['users']), 0)

    def test_profile_list_followers(self):
        """
        /followers GET should return a list of the profiles followers.
        """
        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        # 2 Profiles should follow the same profile.
        profile = Profile.objects.get(id=self.test_profile2.id)
        profile.follow_user(self.test_profile.id)
        profile.save()
        profile2 = Profile.objects.get(id=self.test_profile3.id)
        profile2.follow_user(self.test_profile.id)
        profile2.save()

        response = self.client.get('/api/v1/users/{}/followers/'.format(self.test_profile.id), format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 2)
        self.assertEqual(response.data['users'][0]['id'], profile.id)
        self.assertEqual(response.data['users'][1]['id'], profile2.id)

        profile2.followed_profiles.clear()
        profile2.save()

        response = self.client.get('/api/v1/users/{}/followers/'.format(self.test_profile.id), format="json")
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['id'], profile.id)

    def test_profile_list_followers_empty(self):
        """
        /followers GET should return a list of profiles whom are following the user.
        """
        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/users/{}/followers/'.format(self.test_profile.id), format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 0)

    def test_profile_followers_count_updated(self):
        """
        After adding a follower - followers_count should be updated
        """
        # GRRRR - DJANGO SIGNALS MAKES THIS UNTESTABLE .... They're ASYNC so they fire after
        # The test can check for changes.

    def setUp(self):
        self.client = APIClient()

        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.test_profile2 = Profile(username="test_user2", password="testpass", email="test2@user.com")
        self.test_profile2.save()
        self.test_profile3 = Profile(username="test_user3", password="testpass", email="test3@user.com")
        self.test_profile3.save()
        self.__create_auth_tokens()

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

        self.test_profile3_token = AccessToken.objects.create(
            user=self.test_profile2,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=600),
            token=generate_token(),
            application=self.application
        )
        self.test_profile3.save()

class UserListTestCase(TestCase):

    def test_profile_follow_success(self):
        """
        /Users should not list users
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/users/', format="json")

        self.assertEqual(response.status_code, 405)

    def setUp(self):
        self.client = APIClient()

        self.test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        self.test_profile.save()
        self.test_profile2 = Profile(username="test_user2", password="testpass", email="test2@user.com")
        self.test_profile2.save()
        self.test_profile3 = Profile(username="test_user3", password="testpass", email="test3@user.com")
        self.test_profile3.save()
        self.__create_auth_tokens()

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

        self.test_profile3_token = AccessToken.objects.create(
            user=self.test_profile2,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=600),
            token=generate_token(),
            application=self.application
        )
        self.test_profile3.save()

class UserPatchTestCase(APITestBase):

    def test_profile_update_via_patch_success(self):
        """
        /Users/<id>/Patch/ should allow updating of profile  fields
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.patch('/api/v1/users/{}/'.format(self.test_profile.id), data={
            'password': 'slewfoot',
            'email': 'somenewemail@email.com'
        },format="json")

        self.assertEqual(response.status_code, 200)
        profile = Profile.objects.get(id=self.test_profile.id)
        self.assertEqual(profile.email, 'somenewemail@email.com')

    def test_profile_update_via_patch_failure_on_email_unique_constraint(self):
        """
        /Users/<id>/Patch/ should allow updating of profile  fields
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        self.test_profile2.email = 'emailtoreuse@yup.com'
        self.test_profile2.save()

        response = self.client.patch('/api/v1/users/{}/'.format(self.test_profile.id), data={
            'email': 'emailtoreuse@yup.com'
        },format="json")

        self.assertEqual(response.status_code, 408)

    def setUp(self):
        APITestBase.setUp(self)
        self.client = APIClient()