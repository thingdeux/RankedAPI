# DRF Imports
from rest_framework.test import APIClient
# Django Imports
from django.test import TestCase
# Project Imports
from .models import Profile
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
            'email': 'shouldwork@user.com',
            'unlock_key': '123123'
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'username': 'ishouldwork', 'id': 2, 'is_featured': False,
                                         'email': 'shouldwork@user.com', 'phone_number': None, 'is_partner': False,
                                         'avatar_url': None})
        new_account = Profile.objects.get(id=2)
        self.assertIsNot(new_account.password, None)
        self.assertIsNot(new_account.password, "")

        # self.assertEqual(check_password('mo343re', new_account.password), True)

        # auth_response = self.client.post('/api/v1/users/auth/token/', {
        #     "username": "ishouldwork", "password": "mo3435re", "client_id": self.application.client_id,
        #     "grant_type": "password"})
        #
        # self.assertEqual(auth_response.status_code, 200)

    def test_registration_email_exists(self):
        """
        Email is unique - verify two exact emails can't exist.
        """
        response = self.client.post('/api/v1/users/register/', {
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

        # self.test_profile_token = AccessToken.objects.create(
        #     user=self.test_profile,
        #     scope='read write',
        #     expires=timezone.now() + timedelta(seconds=600),
        #     token=generate_token(),
        #     application=self.application
        # )
        # self.test_profile_token.save()


# class ProfileAuthTestCase(TestCase):
#     def get_access_token(self):
#         auth_response = self.client.post('/api/v1/users/auth/token/',
#                                     {"username": "testme", "password": "test",
#                                      "client_id": self.application.client_id,
#                                      "grant_type": "password"})
#
#         return response.data.get("access_token")
#
#     def setUp(self):
#         self.client = APIClient()
#         self.application = Application.objects.get(pk=1)
#         self.user = self.create_user()
#         self.access_token = self.get_access_token()
#
# #         self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.access_token))

class UsersMeTestCase(TestCase):
    def test_me_success(self):
        """
        Profile /me test
        """

        auth_token = "Bearer {}".format(self.test_profile_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.get('/api/v1/users/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
             {
                'me': {
                    'id': 1,
                    'email': 'test@user.com',
                    'avatar_url': None,
                    'is_partner': False,
                    'is_featured': False,
                    'phone_number': None,
                    'username': 'test_user'},
                'videos': []
              })

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

        self.test_profile_token = AccessToken.objects.create(
            user=self.test_profile,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=600),
            token=generate_token(),
            application=self.application
        )
        self.test_profile_token.save()