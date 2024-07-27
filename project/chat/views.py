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
from authentication.models import *



class ChatSettings(View):
    template_name = 'chat/chat_settings.html'

    def get(self, request):
        return render(request, self.template_name)