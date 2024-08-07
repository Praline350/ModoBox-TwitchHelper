from django.contrib import admin
from board.models import *

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['title']
