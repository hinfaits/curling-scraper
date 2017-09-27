import logging
from datetime import date, time, datetime, timedelta
import md5

import dateutil.parser
from bs4 import BeautifulSoup

from app.events.draw import Draw
from app.events.slam import Slam
from app.sites.base import BaseSite
from app import utils

class Gsoc(BaseSite):
    """Scraping for The Grand Slam of Curling"""
    
    def scrape(self, cache=True):
        slams = []

        html = utils.get_url(self.url)
        soup = BeautifulSoup(html, "html.parser")

        target = soup.find_all("div", { "class" : "column" })
        target = target.pop()

        names = target.findAll("h5")
        schedules = target.findAll("tbody")
        for name, schedule in zip(names, schedules):
            slam = Slam(draw_duration=timedelta(hours=2, minutes=30))
            slam.name = "GSOC " + name.text.title()
            next = schedule.findNext("tr")
            while True:
                try:
                    row = next.findAll("td")
                    if "odd" in next.attrs["class"]:
                        date = dateutil.parser.parse(row[0].text).date()
                        # Sloppy logic for determining the implicit year
                        if date.month < 7 and date.today().month > 6:
                            date = date.replace(year=date.today().year + 1)
                    elif "even" in next.attrs["class"]:
                        time = dateutil.parser.parse(row[1].text).time()
                        dt = datetime.combine(date, time)
                        dt = utils.eastern_to_utc(dt)
                        draw = Draw()
                        draw.name = row[0].text
                        draw.datetime = dt
                        draw.network = row[3].text
                        slam.add_draw(draw)
                except KeyError:
                    break
                except AttributeError:
                    break
                next = next.findNext("tr")
            slams.append(slam)

        self.slams = slams
        self.last_scraped = datetime.now()
        if cache:
            self.save_to_cache()

        return self.slams
