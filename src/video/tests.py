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
from oauth2_provider.models import Application, AccessToken
# Standard Library Imports
from datetime import timedelta


class VideoRankingAPICase(TestCase):

    def test_ranking_success(self):
        """
        Account creation success
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/rank/'.format(self.video1.id), {
            'rank_amount': 14
        }, format='json')

        latest_ranking = Ranking.objects.get(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 200)

        # Any Rank amount over 10 should just be set to 10
        self.assertEqual(latest_ranking.rank_amount, 10)
        self.assertEqual(latest_ranking.related_profile, self.test_profile2)
        self.assertEqual(latest_ranking.video, self.video1)

    def test_ranking_rank_amount_is_zero(self):
        """
        Account creation success
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/rank/'.format(self.video1.id), {
            'rank_amount': 0
        }, format='json')

        latest_ranking = Ranking.objects.get(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 200)
        # Any Rank amount over 10 should just be set to 10
        self.assertEqual(latest_ranking.rank_amount, 1)

    def test_ranking_already_exists(self):
        """
        If a video has already been ranked by a given user - they may not re-rank it.
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        new_ranking = Ranking.objects.create(video=self.video1, related_profile=self.test_profile2, rank_amount=10)
        new_ranking.save()

        response = self.client.post('/api/v1/videos/{}/rank/'.format(self.video1.id), {
            'rank_amount': 1
        }, format='json')

        self.assertEqual(response.status_code, 304)
        new_ranking.delete()

    def test_ranking_delete(self):
        """
        Users can remove ranking for a given video.
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        new_ranking = Ranking.objects.create(video=self.video1, related_profile=self.test_profile2, rank_amount=10)
        new_ranking.save()

        response = self.client.delete('/api/v1/videos/{}/rank/'.format(self.video1.id), format='json')

        self.assertEqual(response.status_code, 200)

        new_ranking = list(Ranking.objects.filter(video=self.video1, related_profile=self.test_profile2))
        self.assertEqual(len(new_ranking), 0)

    def test_ranking_video_not_found(self):
        """
        Users can remove ranking for a given video.
        """
        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/rank/'.format(123123123123), format='json')

        self.assertEqual(response.status_code, 404)

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


class VideoCommentAPICase(TestCase):

    def test_comment_success(self):
        """
        User should be able to comment on a Video
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1.id), {
            'comment': 'I love her voice, lyrics though, no good'
        }, format='json')

        latest_comment = Comment.objects.get(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(latest_comment.video, self.video1)
        self.assertEqual(latest_comment.text, 'I love her voice, lyrics though, no good')

    def test_multiple_comments_success(self):
        """
        User should be able to create multiple comments per video.
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1.id), {
            'comment': 'I love his voice, lyrics though, no good'
        }, format='json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1.id), {
            'comment': 'I hate his voice'
        }, format='json')

        self.assertEqual(response.status_code, 200)

        latest_comments = Comment.objects.filter(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(latest_comments.count(), 2)

    def test_comment_failure_on_video_not_found(self):
        """
        User should not be able to leave a comment on a non-existent video
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(12354555), {
            'comment': 'I love her voice, lyrics though, no good'
        }, format='json')

        latest_comment = Comment.objects.filter(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(latest_comment.count(), 0)

    def test_comment_failure_on_comment_not_long_enough(self):
        """
        User should not be able to leave an empty comment on a non-existent video
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1.id), {
            'comment': ''
        }, format='json')

        latest_comment = Comment.objects.filter(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(latest_comment.count(), 0)
        self.assertEqual(response.data, {'description': 'Comment Length too short'})

    def test_comment_failure_on_comment_too_long(self):
        """
        User should not be able to leave an empty comment on a non-existent video
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        characters_540 = 'j9udVl67ueTHPUgU8UD7ue0LjtTXTgYH8KgqnGWXcY2D7KhKJUS4w7BIsuUaFUYlbyHNoEK9k0u3kBbQOfNMQ' \
                          'oohF4wD7aHvmsi5tUMF40W93FDF5lcMt8BJv2k5yTckQ4MrA1yyt9I286W7s3my1nZBeREBmaf3HbheeBIauy' \
                          'u5QQWrwaOuP2D6eBWCofvQdjmTOAY7aItHJPnrJeewDgA5b8cbzFccT1bMn27SEPAHQgyuMCMgK3udlwRrA9a' \
                          'dljcktrsO3M9ba1uRkBSEhttOEmpHWJHkNfl2JIBPwgup277Gqvk2NiMSuNurPlkowrA2Bpo98ZN1wUnbAwOx' \
                          'NgIT5U80vvPhttNSu6aPOM9VVpueAG2PZoF6rUbXMQlx3NwzKqVB9aysKd27EO263ZJR46MeFEv82E5RyTPnp' \
                          'ohfNAqBOta9WCCobawUGZ9ZMtQ5nScgMVibvfyuXX7dcIH731GUGrvOMtPSyIArlBnQUNI07JPtJjwwCVT36OrfLYdM'

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1), {
            'comment': characters_540
        }, format='json')

        latest_comment = Comment.objects.filter(video=self.video1, related_profile=self.test_profile2)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'description': 'Comment Length exceeds 512 characters'})
        self.assertEqual(latest_comment.count(), 0)

    def test_comment_missing_in_request(self):
        """
        User should not be able to leave an empty comment on a non-existent video
        """

        auth_token = "Bearer {}".format(self.test_profile2_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

        response = self.client.post('/api/v1/videos/{}/comments/'.format(self.video1), format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'description': 'Comment Length too short'})


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