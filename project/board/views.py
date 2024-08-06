from django.conf import settings
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import requests
from django.contrib.auth.mixins import LoginRequiredMixin


from chat.views import *

load_dotenv()


class HomeView(LoginRequiredMixin, View):
    template_name = 'board/home.html'

    def get(self, request):
        print("ok")
        user = request.user
        headers = {
            'Authorization': f'Bearer {user.access_token}',
            'Client-Id': settings.TWITCH_CLIENT_ID,
        }
    
        response = requests.get(f'https://api.twitch.tv/helix/channels?broadcaster_id={user.twitch_id}', headers=headers)
        response.raise_for_status()  # This will raise an HTTPError if the response was an error
        channel_info = response.json()['data'][0]
        print(channel_info)
        context = {
            'channel_info': channel_info,
            'user': user,
        }
        return render(request, 'board/home.html', context=context)

