# Create your views here.
from datetime import timedelta

import requests
from django.http import HttpResponse
from django.template import loader
from weather.utils import *
from django.conf import settings
from scraping.models import SnowLocation
from random import choice
from FlakeFinder.secrets import GOOGLE_MAPS_KEY


def index(request):
    template = loader.get_template('weather/index.html')
    cutoff = datetime.now() - timedelta(hours=3)
    query = SnowLocation.objects.filter(snow_now=True, updated_at__gt=cutoff)
    # random_item = choice(query)
    random_item = {"lat": 12.78, "lng": -12.45, "name": "Puerto Rico"}
    context = {
        'api_key': GOOGLE_MAPS_KEY,
        'lat': random_item["lat"],
        'lng': random_item["lng"],
        'name': random_item["name"]
    }
    return HttpResponse(template.render(context, request))


def forecast(request, lat, lon):
    lat, lon = check_valid_coords(lat, lon)

    if check_in_conus(lat, lon):
        conus = True
    else:
        conus = False

    f = get_forecast(lat, lon)
    snow_times = get_snow_times(f)
    if len(snow_times) == 0:
        return HttpResponse("No snow!")

    flakes = []
    for time in snow_times:
        url = get_sounding_url(lat, lon, time, conus)
        sounding = parse_sounding(url)

        if sounding is None:
            return HttpResponse("No data!")

        layer_df = get_snow_layer(sounding)
        predict_snowflake_shape(layer_df)


def random(request):
    pass
    # query = SnowLocation.objects.filter(snow_now=True,
    #                                     updated_at__gt=datetime.now() - \
    #                                     timedelta(hours=3))
    # random_item = choice(query)
    # forecast(request, random_item["lat"], random_item["lng"])
