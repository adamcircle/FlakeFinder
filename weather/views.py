from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django import forms
import requests
from .models import Soundings


def index(request):
    return HttpResponse("Hello world.")


def forecast(request, lat, lon):
    page = requests.get(url)
    return HttpResponse("Hello world.")
