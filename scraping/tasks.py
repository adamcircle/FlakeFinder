from scraping.scraper import *
from FlakeFinder.celery import app


@app.task
def update_snow_locs():
    locs = scrape_snow_locs()
    for i in range(len(locs)):
        try:
            loc = SnowLocation.objects.get(og_name=locs[i])
            locs[i] = loc["lat"], loc["lon"], loc["name"], locs[i]
        except ObjectDoesNotExist:
            locs[i] = geocode(locs[i])
    save_snow_locs(locs)
    reset_snow_status()
