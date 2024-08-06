from django.db import models
from django.contrib.auth.models import AbstractUser


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

    @classmethod
    def create_or_update_user(cls, user_info, access_token, refresh_token, token_expires):
        twitch_id = user_info['id']
        email = user_info['email']
        display_name = user_info['display_name']

        user, created = cls.objects.get_or_create(email=email, defaults={
            'username': user_info['login'],
            'twitch_id': twitch_id,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires': token_expires,
            'display_name': display_name,
        })

        if not created:
            # Mise à jour des informations de l'utilisateur existant
            user.access_token = access_token
            user.refresh_token = refresh_token
            user.token_expires = token_expires
            user.display_name = display_name
            user.save()

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