# DRF Imports
from rest_framework.test import APIClient
# Django Imports
from django.test import TestCase
# Project Imports
from .models import Profile

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
        test_profile = Profile(username="test_user", password="testpass", email="test@user.com")
        test_profile.save()


# class ProfileAuthTestCase(TestCase):
#     def get_access_token(self):
#         response = self.client.post('/api/v1/users/auth/token/',
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
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.access_token))