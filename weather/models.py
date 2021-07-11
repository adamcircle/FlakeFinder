from django.db import models


# Create your models here.
class Soundings(models.Model):
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    temp = models.DecimalField(max_digits=4, decimal_places=1)
    dewpt = models.DecimalField(max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
