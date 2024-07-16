from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    twitch_id = models.CharField(max_length=50, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)
