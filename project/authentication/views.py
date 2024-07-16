import requests
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from authentication.models import User
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

load_dotenv()


@login_required
def home(request):
    user = request.user
    headers = {
        'Authorization': f'Bearer {user.access_token}',
        'Client-Id': settings.TWITCH_CLIENT_ID,
    }
    response = requests.get(f'https://api.twitch.tv/helix/channels?broadcaster_id={user.twitch_id}', headers=headers)
    channel_info = response.json()['data'][0]
    return render(request, 'board/home.html', {'channel_info': channel_info})

def login_view(request):
    return render(request, 'authentication/login.html')

@login_required
def logout_user(request):
    """Log out the user and redirect to the login page."""
    logout(request)
    return redirect("login")

def twitch_auth(request):
    client_id = os.getenv('TWITCH_CLIENT_ID')
    redirect_uri = settings.TWITCH_REDIRECT_URI
    scope = "user:read:email chat:read chat:edit"
    response_type = "code"

    auth_url = (
        f"https://id.twitch.tv/oauth2/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope}"
    )

    return redirect(auth_url)

def twitch_callback(request):
    code = request.GET.get('code')
    if code:
        token_url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': os.getenv('TWITCH_CLIENT_ID'),
            'client_secret': os.getenv('TWITCH_CLIENT_SECRET'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.TWITCH_REDIRECT_URI,
        }
        response = requests.post(token_url, data=data)
        response_data = response.json()
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        expires_in = response_data.get('expires_in')
        token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': os.getenv('TWITCH_CLIENT_ID'),
        }
        user_info_response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
        user_info = user_info_response.json()['data'][0]
        twitch_id = user_info['id']
        email = user_info['email']

        user, created = User.objects.get_or_create(email=email, defaults={
            'username': user_info['login'],
            'twitch_id': twitch_id,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires': token_expires,
            
        })

        if not created:
            user.access_token = access_token
            user.refresh_token = refresh_token
            user.token_expires = token_expires
            user.save()

        login(request, user)
        return redirect('home')

    return render(request, 'error.html', {'message': 'Failed to authenticate with Twitch'})