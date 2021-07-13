# Create your views here.
from django.http import HttpResponse
from django.template import loader
from weather.utils import *
from django.conf import settings


def index(request):
    template = loader.get_template('weather/index.html')
    context = {
        'api_key': settings.GOOGLE_MAPS_KEY
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
