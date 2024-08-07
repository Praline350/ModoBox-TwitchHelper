from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class UserChatSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#ffffff')
    font_color = models.CharField(max_length=7, default='#000000')

        
    def __str__(self):
        return f"{self.user.username}'s chat settings"
    


class ChatMessage(models.Model):
    username = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.message[:30]} ({self.timestamp})'
    
    
    class Meta:
        ordering = ['-timestamp'] 