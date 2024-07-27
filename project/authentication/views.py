import requests
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from django.urls import reverse
from authentication.models import User
from django.utils import timezone
from rest_framework import status
import datetime
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

load_dotenv()
    

def login_view(request):
    return render(request, 'authentication/login.html')

@login_required
def logout_user(request):
    """Log out the user and redirect to the login page."""
    logout(request)
    return redirect("login")

# Vue pour démarrer l'authentification avec Twitch
class TwitchAuth(APIView):
    def get(self, request):
        client_id = settings.TWITCH_CLIENT_ID
        redirect_uri = settings.TWITCH_REDIRECT_URI
        scope = "user:read:email chat:read chat:edit"
        response_type = "code"
        # URL pour la redirection vers l'authentification Twitch
        auth_url = (
            f"https://id.twitch.tv/oauth2/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type={response_type}"
            f"&scope={scope}"
        )
        return redirect(auth_url)

# Callback pour traiter la réponse de Twitch après l'authentification
class TwitchCallback(APIView):
    def get(self, request):
        code = request.GET.get('code')
        if code:
            token_url = "https://id.twitch.tv/oauth2/token"
            data = {
                'client_id': settings.TWITCH_CLIENT_ID,
                'client_secret': settings.TWITCH_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.TWITCH_REDIRECT_URI,
            }
            # Demande de jeton d'accès à Twitch
            response = requests.post(token_url, data=data)
            response_data = response.json()
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')
            expires_in = response_data.get('expires_in')
            token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)

            # Préparation des en-têtes pour l'appel API à Twitch pour obtenir les informations de l'utilisateur
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Client-Id': settings.TWITCH_CLIENT_ID,
            }
            user_info_response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
            user_info = user_info_response.json()['data'][0]

            # Création ou mise à jour de l'utilisateur
            user = create_or_update_user(user_info, access_token, refresh_token, token_expires)
            
            login(request, user)
            return redirect('home')

        # Affichage d'une erreur si l'authentification a échoué
        return render(request, 'error.html', {'message': 'Failed to authenticate with Twitch'})


def create_or_update_user(user_info, access_token, refresh_token, token_expires):
    twitch_id = user_info['id']
    email = user_info['email']
    display_name = user_info['display_name']

    user, created = User.objects.get_or_create(email=email, defaults={
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