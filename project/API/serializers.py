from rest_framework import serializers
from chat.models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['user', 'username', 'message','timestamp']

    def get_username(self, obj):
        return obj.user.username
    
    def get_message(self, obj):
        # Nettoyer les caractères de nouvelle ligne
        return obj.message.replace('\r', '').replace('\n', '')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'display_name', 'access_token']


class UserChatSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatSettings
        fields = ['background_color', 'font_color']