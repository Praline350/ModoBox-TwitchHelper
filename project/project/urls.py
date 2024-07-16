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

from authentication.views import *
from authentication.api_views import *
from chat.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication by twitch
    path('twitch/auth/', twitch_auth, name='twitch_auth'),
    path('twitch/callback/', twitch_callback, name='twitch_callback'),
    path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/chat/', start_chat, name='chat'),

    # API
    path('api/get-token/', get_token, name='api_get_token'),
]
