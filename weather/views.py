# Create your views here.
from datetime import timedelta
from django.http import HttpResponse
from django.template import loader
from weather.utils import *
from django.conf import settings
from scraping.models import SnowLocation
from random import choice


def index(request):
    template = loader.get_template('weather/index.html')
    cutoff = datetime.now() - timedelta(hours=3)
    query = SnowLocation.objects.filter(snow_now=True, updated_at__gt=cutoff)
    # random_item = choice(query)
    random_item = {"lat": 12.78, "lng": -12.45, "name": "Puero Rico"}
    context = {
        'api_key': GOOGLE_MAPS_KEY,
        'lat': random_item["lat"],
        'lng': random_item["lng"],
        'name': random_item["name"]
    }
    return HttpResponse(template.render(context, request))


def forecast(request, lat, lon):
    lat, lon = check_valid_coords(lat, lon)

    f = get_forecast(lat, lon)
    snow = get_snow_data(f)
    if snow is None:
        return HttpResponse("Hello world.")


def random(request):
    pass
    # query = SnowLocation.objects.filter(snow_now=True,
    #                                     updated_at__gt=datetime.now() - \
    #                                     timedelta(hours=3))
    # random_item = choice(query)
    # forecast(request, random_item["lat"], random_item["lng"])
