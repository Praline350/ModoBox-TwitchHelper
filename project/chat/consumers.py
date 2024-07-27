import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'

        # Joindre le groupe
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recevoir un message du WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        # Enregistrer le message dans la base de données
        user = self.scope['user']
        

        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Recevoir un message du groupe
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))