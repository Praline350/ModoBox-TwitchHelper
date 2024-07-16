from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
import os
from django.utils import timezone
import datetime
from dotenv import load_dotenv
from django.test.utils import override_settings
from django.conf import settings
from unittest.mock import patch

User = get_user_model()
load_dotenv()


class TwitchAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.twitch_auth_url = reverse('twitch_auth')
        self.twitch_callback_url = reverse('twitch_callback')

    @override_settings(
        TWITCH_CLIENT_ID=os.getenv('TWITCH_CLIENT_ID'),
        TWITCH_CLIENT_SECRET=os.getenv('TWITCH_CLIENT_SECRET'),
        TWITCH_REDIRECT_URI=os.getenv('TWITCH_REDIRECT_URI')
    )

    def test_twitch_auth_redirect(self):
        response = self.client.get(self.twitch_auth_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('https://id.twitch.tv/oauth2/authorize'))
        self.assertIn('client_id=' + os.getenv('TWITCH_CLIENT_ID'), response.url)
        self.assertIn('redirect_uri=' + os.getenv('TWITCH_REDIRECT_URI'), response.url)
        self.assertIn('response_type=code', response.url)
        self.assertIn('scope=user:read:email', response.url)

    @patch('requests.post')
    @patch('requests.get')
    def test_twitch_callback_new_user(self, mock_get, mock_post):
        # Mock the response from Twitch for token
        mock_post.return_value.json.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_in': 3600
        }

        # Mock the response from Twitch for user info
        mock_get.return_value.json.return_value = {
            'data': [{
                'id': 'test_twitch_id',
                'login': 'testuser',
                'email': 'testuser@example.com'
            }]
        }

        # Simuler une requête GET vers la vue twitch_callback avec un code
        response = self.client.get(self.twitch_callback_url, {'code': 'test_code'})

        # Vérifier que l'utilisateur a été créé dans la base de données
        user = User.objects.get(email='testuser@example.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.twitch_id, 'test_twitch_id')
        self.assertEqual(user.access_token, 'test_access_token')
        self.assertEqual(user.refresh_token, 'test_refresh_token')

        # Vérifier que l'utilisateur est redirigé vers la page d'accueil
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))