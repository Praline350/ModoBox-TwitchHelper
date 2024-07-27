from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    twitch_id = models.CharField(max_length=50, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires = models.DateTimeField(blank=True, null=True)
    display_name = models.CharField(max_length=60, blank=True, null=True)
    

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)


class Streamer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streamer')
    channel_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.channel_name = self.user.username
        super(Streamer, self).save(*args, **kwargs)

    def __str__(self):
        return self.channel_name


class Moderator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderate')
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE, related_name='moderators')
    # Ajoutez d'autres champs spécifiques aux modérateurs ici

    def __str__(self):
        return f'{self.user.username} - {self.streamer.channel_name}'