# chat/consumers.py
import json
import asyncio
import websocket
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import User
from channels.db import database_sync_to_async
from chat.models import ChatMessage


CHAT_SERVER = 'wss://irc-ws.chat.twitch.tv:443'

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'

        # Joindre le groupe
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Démarrer la connexion WebSocket à Twitch dans un thread séparé
        asyncio.create_task(self.connect_to_twitch())

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def connect_to_twitch(self):
        loop = asyncio.get_running_loop()
        def on_message(ws, message):
            loop.call_soon_threadsafe(asyncio.create_task, self.handle_twitch_message(message))

        def on_error(ws, error):
            print(f"Erreur: {error}")

        def on_close(ws):
            print("### Connection fermée ###")

        def on_open(ws):
            print("Connexion ouverte")
            ws.send(f"PASS oauth:{self.scope['user'].access_token}")
            ws.send(f"NICK {self.scope['user'].username}")
            ws.send(f"JOIN #{self.scope['user'].username}")

        ws = websocket.WebSocketApp(
            CHAT_SERVER,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.on_open = on_open
        await loop.run_in_executor(None, ws.run_forever)

    async def handle_twitch_message(self, message):
        # Traiter le message reçu de Twitch et l'envoyer au groupe
        if "PRIVMSG" in message:
            parts = message.split(":", 2)
            user_info = parts[1].split("!")
            username = user_info[0]
            chat_message = parts[2]

            # Enregistrer le message dans la base de données
           
            await self.create_chat_message(username, chat_message)

            # Envoyer le message au groupe
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': chat_message,
                    'username': username
                }
            )


    @database_sync_to_async
    def create_chat_message(self, username, message):
        user, _ = User.objects.get_or_create(username=username)
        ChatMessage.objects.create(user=user,  message=message)