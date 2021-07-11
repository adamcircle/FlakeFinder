import pprint
from datetime import datetime
import requests
from FlakeFinder.secrets import OWM_KEY
import pandas as pd
import io
import json


def get_sounding_url(lat, lon, time):
    """
    Gets the url for the sounding at the specified place and time
    :param lat: Latitude
    :param lon: Longitude
    :return: String, url
    """
    now = datetime.now()
    year = now.year
    month = now.strftime('%B')[:3]
    day = now.day
    hour = now.hour
    lat = round(lat, 2)
    lon = round(lon, 2)
    url = f"https://rucsoundings.noaa.gov/get_soundings.cgi?" \
          f"data_source=Op40" \
          f"&latest=latest" \
          f"&start_year={year}" \
          f"&start_month_name={month}" \
          f"&start_mday={day}" \
          f"&start_hour={hour}" \
          f"&start_min=0" \
          f"&n_hrs=1.0" \
          f"&fcst_len=shortest" \
          f"&airport={lat}%2C{lon}" \
          f"&text=Ascii%20text%20%28GSL%20format%29" \
          f"&hydrometeors=false" \
          f"&start=latest"

    return url


def get_forecast(lat, lon):
    """
    Calls the OWM api to get the forecast at the specified location
    :param lat: Latitude
    :param lon: Longitude
    :return: dict, parsed json forecast
    """

    url = f"https://api.openweathermap.org/data/2.5/forecast?" \
          f"lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
    data = requests.get(url).text
    parsed = json.loads(data)
    return parsed


def get_snow_data(forecast_json):
    pass


def parse_forecast():
    pass


def parse_sounding(url):
    """
    Get sounding from rucsoundings.noaa.gov and parse it into a dataframe
    :param url: String
    :return: Dataframe, sounding
    """
    # url = "https://rucsoundings.noaa.gov/get_soundings.cgi?data_source=Op40&latest=latest&start_year=2021&start_month_name=Jul&start_mday=10&start_hour=2&start_min=0&n_hrs=1.0&fcst_len=8&airport=36.77%2C-119.72&text=Ascii%20text%20%28GSL%20format%29&hydrometeors=false&start=latest"
    file = io.StringIO(requests.get(url).text)
    # with open("weather/sounding_example.txt", "r") as f:
    # print(f.readline())
    col_names = ("Type", "Pressure", "Height",
                 "Temp", "Dewpt", "WindDir", "WindSpd")
    sounding = pd.read_csv(file,
                           skiprows=7,
                           header=None,
                           names=col_names,
                           delimiter=' ',
                           skipinitialspace=True,
                           error_bad_lines=False,
                           keep_default_na=False,
                           na_values="99999")
    sounding['Temp'] = sounding['Temp'].map(lambda temp: temp / 10)
    sounding['Dew_pt'] = sounding['Dew_pt'].map(lambda dew_pt: dew_pt / 10)
    return sounding
