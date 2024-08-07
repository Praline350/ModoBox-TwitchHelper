"""
URL configuration for project project.

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from authentication.views import *
from board.views import *
from API.views import *
from chat.views import *



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
    path('board/<str:user>/stream_manager', StreamManager.as_view(), name='stream_manager'),
    

    # Chat
    path('chat/settings/', ChatSettings.as_view(), name='chat_settings'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)