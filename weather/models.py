from django.db import models


# Create your models here.
class Sounding(models.Model):
    forecast_date = models.DateTimeField()
