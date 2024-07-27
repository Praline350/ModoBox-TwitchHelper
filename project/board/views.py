import requests
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login
from authentication.models import User
from django.utils import timezone
import datetime
import requests
import websocket
import threading
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

from chat.utils import *
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
        context = {
            'channel_info': channel_info,
            'user': user,
        }
        start_twitch_chat(user)
        return render(request, 'board/home.html', context=context)

