from django.contrib import admin
from chat.models import *

@admin.register(UserChatSettings)
class AdminUserChatSettings(admin.ModelAdmin):
    list_display = ['user', ]

@admin.register(ChatMessage)
class AdminChatMessage(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp']
