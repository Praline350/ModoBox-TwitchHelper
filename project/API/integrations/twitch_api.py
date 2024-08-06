import requests
from django.conf import settings
from django.utils import timezone
import datetime

class TwitchAPI:
    def __init__(self):
        self.client_id = settings.TWITCH_CLIENT_ID
        self.client_secret = settings.TWITCH_CLIENT_SECRET
        self.redirect_uri = settings.TWITCH_REDIRECT_URI
        self.base_url = "https://api.twitch.tv/helix"
    
    def get_access_token(self, code):
        token_url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        }
        response = requests.post(token_url, data=data)
        response_data = response.json()
        return response_data

    def get_user_info(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
        }
        user_info_url = f"{self.base_url}/users"
        response = requests.get(user_info_url, headers=headers)
        response_data = response.json()
        return response_data.get('data')[0]

    def refresh_access_token(self, refresh_token):
        token_url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        response = requests.post(token_url, data=data)
        response_data = response.json()
        return response_data
