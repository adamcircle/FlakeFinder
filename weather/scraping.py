from bs4 import BeautifulSoup
import requests
import pycountry


def get_snow_spots():
    """
    Find up to 20 places in the world where it is currently snowing using
    snow-forecast.com.
    :return: List, locations and country code
    """
    URL = "https://www.snow-forecast.com/overviews/picks"
    page = requests.get(URL)

    locs = []

    soup = BeautifulSoup(page.content, "html.parser")
    table_title = soup.find(text="Fresh Snow Depth")
    table = table_title.parent.parent
    links = table.find_all("a")
    flags = table.find_all("i")

    for i in range(max(len(flags), 20)):
        countrycode = flags[i]["class"][1].replace("flag-", "")
        country = pycountry.countries.get(alpha_2=countrycode)
        loc = links[i].text
        if "(" in loc:
            loc = loc.split("(")[0].strip()
        loc += ", " + country.name
        locs.append(loc)
    return locs
