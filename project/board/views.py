from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.views import *
from API.integrations.twitch_api import *
from board.forms import *

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
    template_name = 'board/forms/create_prediction.html'

    def post(self, request):
        user = request.user
        broadcaster_id = user.twitch_id
        access_token = user.access_token
        form = PredictionForm(request.POST)
        formset = OutcomeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            twitch_api = TwitchAPI()
            title = form.cleaned_data['title']
            prediction_window = form.cleaned_data['prediction_window']
            outcomes = [outcome_form.cleaned_data['title'] for outcome_form in formset if outcome_form.cleaned_data]
            data = {
                "title": title,
                "outcomes": [{"title": outcome} for outcome in outcomes],
                "prediction_window": prediction_window
            }
            response = twitch_api.post_prediction(broadcaster_id, access_token, data)
            print(response)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': form, 'formset':formset})
            
            

    def get(self, request):
        form = PredictionForm()
        formset = OutcomeFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

