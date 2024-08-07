from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()

class UserModelTests(TestCase):

    def setUp(self):
        self.user_info = {
            'id': 'test_twitch_id',
            'login': 'testuser',
            'email': 'testuser@example.com',
            'display_name': 'TestUser',
            'profile_image_url': 'http://example.com/profile.jpg'
        }
        self.access_token = 'test_access_token'
        self.refresh_token = 'test_refresh_token'
        self.token_expires = timezone.now() + datetime.timedelta(seconds=3600)

    def test_create_new_user(self):
        # Appel de la méthode pour créer un nouvel utilisateur
        user = User.create_or_update_user(self.user_info, self.access_token, self.refresh_token, self.token_expires)

        # Vérifier que l'utilisateur a été créé dans la base de données
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.display_name, 'TestUser')
        self.assertEqual(user.twitch_id, 'test_twitch_id')
        self.assertEqual(user.profile_image_url, 'http://example.com/profile.jpg')
        self.assertEqual(user.access_token, 'test_access_token')
        self.assertEqual(user.refresh_token, 'test_refresh_token')
        self.assertEqual(user.token_expires, self.token_expires)

    def test_update_existing_user(self):
        # Create the user first
        User.create_or_update_user(self.user_info, self.access_token, self.refresh_token, self.token_expires)

        # Update with new tokens and expiration
        new_access_token = 'new_access_token'
        new_refresh_token = 'new_refresh_token'
        new_token_expires = timezone.now() + datetime.timedelta(seconds=7200)

        user = User.create_or_update_user(self.user_info, new_access_token, new_refresh_token, new_token_expires)
        self.assertIsNotNone(user)
        self.assertEqual(user.access_token, new_access_token)
        self.assertEqual(user.refresh_token, new_refresh_token)
        self.assertEqual(user.token_expires, new_token_expires)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.display_name, 'TestUser')
        self.assertEqual(user.twitch_id, 'test_twitch_id')
        self.assertEqual(user.profile_image_url, 'http://example.com/profile.jpg')
