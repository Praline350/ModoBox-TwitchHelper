"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from authentication.views import *
from board.views import *
from API.views import *
from chat.views import *
from chat.utils import *


router = routers.SimpleRouter()
router.register(r'chat/messages', ChatMesssageViewset, basename='chat_message')


urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication by twitch
    path('twitch/auth/', TwitchAuth.as_view(), name='twitch_auth'),
    path('twitch/callback/', TwitchCallback.as_view(), name='twitch_callback'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),

    # API
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/get-token/', GetTokenView.as_view(), name='api_get_token'),
    path('api/chat/settings/', UserChatSettingsDetail.as_view(), name='api_chat_setting'),
    

    # Boards
    path('home/', HomeView.as_view(), name='home'),
    

    # Chat
    # path('chat/', start_chat, name='chat'),
    path('chat/settings/', ChatSettings.as_view(), name='chat_settings'),
]
