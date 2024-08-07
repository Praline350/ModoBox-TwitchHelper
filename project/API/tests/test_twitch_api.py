from django.test import TestCase
from django.test import TestCase
from unittest.mock import patch
from django.conf import settings

from API.integrations.twitch_api  import *


class TwitchAPITests(TestCase):
    def setUp(self):
        self.twitch_api = TwitchAPI()
        self.access_token = 'test_access_token'
        self.broadcaster_id = 'test_broadcaster_id'

    @patch('requests.post')
    def test_get_access_token(self, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_in': 3600
        }
        response = self.twitch_api.get_access_token('test_code')
        self.assertEqual(response['access_token'], 'test_access_token')
        self.assertEqual(response['refresh_token'], 'test_refresh_token')
        self.assertEqual(response['expires_in'], 3600)

    @patch('requests.get')
    def test_get_user_info(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data': [{
                'id': 'test_twitch_id',
                'login': 'testuser',
                'email': 'testuser@example.com',
                'display_name': 'TestUser'
            }]
        }
        response = self.twitch_api.get_user_info(self.access_token)
        self.assertEqual(response['id'], 'test_twitch_id')
        self.assertEqual(response['login'], 'testuser')
        self.assertEqual(response['email'], 'testuser@example.com')
        self.assertEqual(response['display_name'], 'TestUser')

    @patch('requests.get')
    def test_get_subscribers(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data': [
                {'user_id': 'user1', 'user_name': 'User1'},
                {'user_id': 'user2', 'user_name': 'User2'}
            ]
        }
        response = self.twitch_api.get_subscribers(self.broadcaster_id, self.access_token)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['user_id'], 'user1')
        self.assertEqual(response[1]['user_id'], 'user2')