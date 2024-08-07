from django import forms
from django.forms import inlineformset_factory
from  board.models import Prediction, Outcome


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['title', 'prediction_window']

OutcomeFormSet = inlineformset_factory(Prediction, Outcome, fields=['title'], extra=2)