from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
import threading
import websocket
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

from chat.models import *
from chat.utils import *
from authentication.models import *


@login_required
def start_chat(request):
    user = request.user
    ws_thread = start_twitch_chat(user)
    print(f"Thread info: Name={ws_thread.name}, Alive={ws_thread.is_alive()}")
    return render(request, 'chat/twitch_chat.html', {'user': user})



class ChatSettings(View):
    template_name = 'chat/chat_settings.html'

    def get(self, request):
        user = request.user
        start_twitch_chat(user)
        return render(request, self.template_name)