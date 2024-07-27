# chat/twitch_chat.py
import requests
import websocket
import threading
from django.conf import settings
from .models import ChatMessage

CHAT_SERVER = 'wss://irc-ws.chat.twitch.tv:443'

class TwitchChat:
    def __init__(self, user):
        self.user = user
        self.access_token = user.access_token
        self.client_id = settings.TWITCH_CLIENT_ID
        self.chat_server = CHAT_SERVER
        print(f"User: {self.user}, Access Token: {self.access_token}, Client ID: {self.client_id}")

    def get_user_info(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }
        response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
        return response.json()['data'][0]

    def on_message(self, ws, message):
        print(f"Message reçu: {message}")
        if "PRIVMSG" in message:
            parts = message.split(":", 2)
            user_info = parts[1].split("!")
            username = user_info[0]
            chat_message = parts[2]

            # Enregistrer le message dans la base de données
            ChatMessage.objects.create(
                user=self.user,
                message=chat_message
            )

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
        try:
            print("Starting WebSocket connection...")
            ws = websocket.WebSocketApp(self.chat_server,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            ws.on_open = self.on_open
            ws.run_forever()
            print("WebSocket is running")
        except Exception as e:
            print(f"Exception in WebSocket connection: {e}")
