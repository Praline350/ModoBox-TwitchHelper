from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
import requests
import threading
import websocket
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging


# URL de l'endpoint de chat IRC de Twitch
CHAT_SERVER = 'wss://irc-ws.chat.twitch.tv:443'

class TwitchChat:
    def __init__(self, user):
        self.user = user
        self.access_token = user.access_token
        self.client_id = settings.TWITCH_CLIENT_ID
        self.chat_server = CHAT_SERVER

    def get_user_info(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }
        response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
        return response.json()['data'][0]

    def on_message(self, ws, message):
        print(f"Message reçu: {message}")

    def on_error(self, ws, error):
        print(f"Erreur: {error}")

    def on_close(self, ws):
        print("### Connection fermée ###")

    def on_open(self, ws):
        print("Connexion ouverte")
        user_info = self.get_user_info()
        username = user_info['login']

        # S'authentifier sur le chat
        ws.send(f"PASS oauth:{self.access_token}")
        ws.send(f"NICK {username}")
        ws.send(f"JOIN #{username}")

    def start_websocket(self):
        ws = websocket.WebSocketApp(self.chat_server,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

@login_required
def start_chat(request):
    user = request.user

    # Store tokens in session
    request.session['access_token'] = user.access_token
    request.session['username'] = user.username

    twitch_chat = TwitchChat(request.user)
    ws_thread = threading.Thread(target=twitch_chat.start_websocket)
    ws_thread.start()
    return render(request, 'chat/twitch_chat.html', {'user': user})