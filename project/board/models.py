from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Prediction(models.Model):
    title = models.CharField(max_length=100)
    prediction_window = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(1800)])


    def __str__(self):
        return self.title

class Outcome(models.Model):
    prediction = models.ForeignKey(Prediction, related_name='outcomes', on_delete=models.CASCADE)
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title