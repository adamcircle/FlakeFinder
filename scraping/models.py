from django.db import models


# Create your models here.
class SnowLocation(models.Model):
    lat = models.DecimalField(max_digits=6, decimal_places=4)
    lng = models.DecimalField(max_digits=7, decimal_places=4)
    og_name = models.TextField()
    name = models.TextField()
    snow_now = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
