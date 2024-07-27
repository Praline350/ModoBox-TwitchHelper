from rest_framework import serializers
from chat.models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatMessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = ChatMessage
        fields = ['username', 'message', 'timestamp']
    



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'display_name', 'access_token']


class UserChatSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatSettings
        fields = ['background_color', 'font_color']