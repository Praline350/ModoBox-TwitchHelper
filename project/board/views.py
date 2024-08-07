from django.shortcuts import render
from dotenv import load_dotenv
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.views import *
from API.integrations.twitch_api import *

load_dotenv()


class HomeView(LoginRequiredMixin, View):
    template_name = 'board/home.html'

    def get(self, request):
        user = request.user
        broadcaster_id = user.twitch_id
        access_token = user.access_token
        if broadcaster_id and access_token:
            twitch_api = TwitchAPI()
            channel_info = twitch_api.get_channel_info(broadcaster_id, access_token)
            user_info = twitch_api.get_user_info(access_token)
            subscribers = twitch_api.get_subscribers(broadcaster_id, access_token)
            followers = twitch_api.get_followers(broadcaster_id, access_token)

            context = {
                'channel_info': channel_info,
                'user': user,

            }
            return render(request, self.template_name, context=context)
        else:
            return render(request, 'error.html', {'message': 'Failed to retrieve channel information'})



class StreamManager(LoginRequiredMixin, View):
    template_name = 'board/stream_manager.html'

    def get(self, request, user):   # Penser a faie un décorateur pour récuperer broadcaster et acces_token directement ???
        user = request.user
        broadcaster_id = user.twitch_id
        access_token = user.access_token
        if broadcaster_id and access_token:
            twitch_api = TwitchAPI()
            channel_info = twitch_api.get_channel_info(broadcaster_id, access_token)
            followers = twitch_api.get_followers(broadcaster_id, access_token)

            context = {
                'channel_info': channel_info,
                'user': user,
                'followers': followers
            }
            return render(request, self.template_name, context=context)
        else:
            return render(request, 'error.html', {'message': 'Failed to retrieve channel information'})
        

class CreatePrediction(LoginRequiredMixin, View):
    template_name = 'board/create_prediction.html'

    def post(self, request):
        user = request.user
        broadcaster_id = user.twitch_id
        access_token = user.access_token
        context = {
                'user': user,
            }
        return render(request, self.template_name, context=context)

