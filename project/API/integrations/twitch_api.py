import requests
import json
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
        # Renvois les info de l'User 

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
        }
        user_info_url = f"{self.base_url}/users"
        response = requests.get(user_info_url, headers=headers)
        response_data = response.json()
        return response_data.get('data')[0]

    def get_channel_info(self, broadcaster_id, access_token):
        # Renvois les information de la chaine du broadcaster

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
        }
        response = requests.get(f'{self.base_url}/channels?broadcaster_id={broadcaster_id}', headers=headers)
        response_data = response.json()['data'][0]
        return response_data

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

    def get_subscribers(self, broadcaster_id, access_token):
        # Renvois la liste des user sub au broadcaster 

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
        }
        subscribers_url = f"{self.base_url}/subscriptions?broadcaster_id={broadcaster_id}"
        response = requests.get(subscribers_url, headers=headers)
        response_data = response.json()
        return response_data.get('data', [])

    def get_followers(self, broadcaster_id, access_token):
        # Renvois une liste des followers du broadcaster

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
        }
        followers_url = f"{self.base_url}/channels/followers?broadcaster_id={broadcaster_id}"
        response = requests.get(followers_url, headers=headers)
        response_data = response.json()
        return response_data
    
    def post_prediction(self, broadcaster_id, access_token, data):
        """
        Args :
            data = '{
                "title": "Any leeks in the stream?",
                "outcomes": [
                    {
                    "title": "Yes, give it time."
                    },
                    {
                    "title": "Definitely not."
                    }
                ]
        """

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }
        data['broadcaster_id'] = broadcaster_id
        json_data = json.dumps(data)
        prediction_url = f"{self.base_url}/predictions"
        response = requests.post(prediction_url, headers=headers, data=json_data)
        return response.json()

