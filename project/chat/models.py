
from django.db import models
from authentication.models import User


class UserChatSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#ffffff')
    font_color = models.CharField(max_length=7, default='#000000')

        
    def __str__(self):
        return f"{self.user.username}'s chat settings"
    


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:30]} ({self.timestamp})'
    
    
    class Meta:
        ordering = ['-timestamp'] 