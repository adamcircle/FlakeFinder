from bs4 import BeautifulSoup
import requests
import pycountry
from FlakeFinder.secrets import GOOGLE_MAPS_KEY
import json
from scraping.models import SnowLocation
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


def scrape_snow_locs():
    """
    Find up to 20 places in the world where it is currently snowing using
    snow-forecast.com.
    :return: List, locations and country
    """
    url = "https://www.snow-forecast.com/overviews/picks"
    page = requests.get(url)

    locs = []

    soup = BeautifulSoup(page.content, "html.parser")
    table_title = soup.find(text="New snow in next 3 days")
    table = table_title.parent.parent
    links = table.find_all("a")
    flags = table.find_all("i")

    for i in range(max(len(flags), 20)):
        country_code = flags[i]["class"][1].replace("flag-", "")
        country = pycountry.countries.get(alpha_2=country_code)
        loc = links[i].text
        if "(" in loc:
            loc = loc.split("(")[0].strip()
        loc += ", " + country.name
        locs.append(loc)
    return locs


def reset_snow_status():
    cutoff = datetime.now() - timedelta(minutes=5)
    SnowLocation.objects.filter(updated_at__lte=cutoff,
                                snow_now=True).update(snow_now=False)


def geocode(address):
    """
    Get geographic coordinates for an url_address.
    :param address: String, location url_address
    :return: Tuple, latitude, longitude, formatted url_address, original url_address
    """
    url_address = address.replace(" ", "+")
    url = f"https://maps.googleapis.com/maps/api/geocode/json" \
          f"?url_address={url_address}&key={GOOGLE_MAPS_KEY}"
    result = json.loads(requests.get(url).text)
    if result["status"] != "OK":
        return None
    else:
        loc = result["results"][0]["geometry"]["location"]
        return round(loc["lat"], 4), round(loc["lng"], 4), \
               result["results"][0]["formatted_address"], address


def save_snow_locs(loc_list):
    """
    Saves the snow locations into the database
    :param loc_list: List of snow locations (lat, lng, name, og_name)
    :return:
    """

    for loc in loc_list:
        try:
            entry = SnowLocation.objects.get(name=loc[2])
            entry.snow_now = True
            entry.save()
        except ObjectDoesNotExist:
            try:
                entry = SnowLocation.objects.create(
                    lat=loc[0],
                    lng=loc[1],
                    name=loc[2],
                    og_name=loc[3]
                )
                entry.save()
            except Exception as e:
                print('Failed:', e)
                break
