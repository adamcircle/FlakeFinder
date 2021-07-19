from datetime import datetime
import requests
from FlakeFinder.secrets import OWM_KEY
import pandas as pd
import io
import json
import numpy as np
from shapely.geometry import Point
import pickle


def get_sounding_url(lat, lon, time, conus=True):
    """
    Gets the url for the sounding at the specified place and time
    :param lat: Latitude
    :param lon: Longitude
    :param time: Seconds since the epoch
    :param conus: True for OP40 or False for GFS model
    :return: String, url
    """
    if conus:
        model = "Op40"
    else:
        model = "GFS"
    dt = datetime.fromtimestamp(time)
    lat = round(lat, 3)
    lon = round(lon, 3)
    url = f"https://rucsoundings.noaa.gov/get_soundings.cgi?" \
          f"data_source={model}" \
          f"&start_year={dt.year}" \
          f"&start_month_name={dt.strftime('%B')[:3]}" \
          f"&start_mday={dt.day}" \
          f"&start_hour={dt.hour}" \
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


def get_snow_times(jso):
    """
    Determine the times, in seconds since the epoch, when OWM predicts snow
    :param jso: the json response from OWM
    :return: A list of times
    """
    times = []
    for period in jso["list"]:
        if "snow" in period:
            times.append((period["dt"], period["pop"]))
    return times


def check_valid_coords(lat, lon):
    try:
        lat, lon = float(lat), float(lon)
        assert -90.0 <= lat <= 90.0
        assert -180.0 <= lon <= 180.0
    except ValueError as err:
        print("Invalid lat, lon value:", err)
    return lat, lon


def parse_sounding(url):
    """
    Get sounding from rucsoundings.noaa.gov and parse it into a dataframe
    :param url: String
    :return: Dataframe, sounding
    """
    resp = requests.get(url)
    if not resp.ok:
        return None
    file = io.StringIO(resp.text)
    # with open("weather/sounding_example.txt", "r") as f:
    # print(f.readline())
    col_names = ("Type", "Pressure", "Altitude",
                 "Temp", "Dew_pt", "WindDir", "WindSpd")
    sounding = pd.read_csv(file,
                           skiprows=6,
                           header=None,
                           names=col_names,
                           delimiter=' ',
                           skipinitialspace=True,
                           error_bad_lines=False,
                           keep_default_na=False,
                           na_values="99999")
    if sounding.Pressure.iloc[0] == 0:
        return None
    sounding['Temp'] = sounding['Temp'].map(lambda temp: temp / 10)
    sounding['Dew_pt'] = sounding['Dew_pt'].map(lambda dew_pt: dew_pt / 10)
    return sounding.iloc[:, [0, 1, 2, 3, 4]]  # strip the wind data


def get_snow_layer(df):
    """
    Identifies the first range of sounding data which meets the criteria for a
    snow formation layer.
    :param df: The sounding dataframe
    :return: A dataframe containing only the snow layer
    """
    # Credit to BENY: https://stackoverflow.com/a/68430627

    # Ensure pressure is at least 200mb less than surface pressure
    cond1 = df.Pressure.sub(df.Pressure.iloc[0]) <= -200

    # Ensure supersaturation
    cond2 = df.Temp - df.Dew_pt <= 1.0

    # Merge the conditions into a truth table
    conditions = (~(cond1 & cond2)).cumsum()

    # Group data
    grouped_pressure_diff = df.groupby(conditions).Pressure.agg(np.ptp)

    # Ensure snow layer is at least 200mb in altitude
    snow_layer = df[conditions.isin(
        grouped_pressure_diff[grouped_pressure_diff > 200].index
    )].iloc[1:, ]

    return snow_layer


def predict_snowflake_shape(df):
    avg_temp = df["Temp"].mean()
    pass


def check_in_conus(lat, lon):
    path = "weather/usa.pickle"
    with open(path, "rb") as poly_file:
        usa = pickle.load(poly_file)
        point = Point(lon, lat)
        return usa.contains(point)
