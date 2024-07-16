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
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from chat.views import start_chat

load_dotenv()


@login_required
def home(request):
    user = request.user
    headers = {
        'Authorization': f'Bearer {user.access_token}',
        'Client-Id': settings.TWITCH_CLIENT_ID,
    }
    response = requests.get(f'https://api.twitch.tv/helix/channels?broadcaster_id={user.twitch_id}', headers=headers)
    channel_info = response.json()['data'][0]
    context = {
        'channel_info': channel_info,
        'user': user,
    }

    # Démarrer le chat Twitch dans un thread séparé
    start_chat(request)
    return render(request, 'board/home.html', context=context)
