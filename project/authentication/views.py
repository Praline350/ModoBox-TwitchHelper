from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

from authentication.models import User
from API.integrations.twitch_api import *

load_dotenv()
    

def login_view(request):
    return render(request, 'authentication/login.html')

@login_required
def logout_user(request):
    """Log out the user and redirect to the login page."""
    logout(request)
    return redirect('login')

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
            twitch_api = TwitchAPI()
            response_data = twitch_api.get_access_token(code)
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')
            expires_in = response_data.get('expires_in')
            token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)

            user_info = twitch_api.get_user_info(access_token)
            user = User.create_or_update_user(user_info, access_token, refresh_token, token_expires)
            
            login(request, user)
            return redirect('home')

        # Affichage d'une erreur si l'authentification a échoué
        return render(request, 'error.html', {'message': 'Failed to authenticate with Twitch'})


