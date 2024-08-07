from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
import requests
from PIL import Image



class User(AbstractUser):
    twitch_id = models.CharField(max_length=50, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires = models.DateTimeField(blank=True, null=True)
    display_name = models.CharField(max_length=60, blank=True, null=True)
    profile_image_url = models.URLField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)

    def save_profile_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = f"profile_images/{self.username}.jpg"
            self.profile_image.save(filename, ContentFile(response.content), save=False)
            self.save()

    @classmethod
    def create_or_update_user(cls, user_info, access_token, refresh_token, token_expires):
        defaults = {
            'username': user_info['login'],
            'twitch_id': user_info['id'],
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires': token_expires,
            'display_name': user_info['display_name'],
            'profile_image_url': user_info['profile_image_url']
        }
        
        user, created = cls.objects.update_or_create(email=user_info['email'], defaults=defaults)
        if user_info.get('profile_image_url'):
            user.save_profile_image(user_info['profile_image_url'])
        return user


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