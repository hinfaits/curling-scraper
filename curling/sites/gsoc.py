import logging
from datetime import date, datetime, timedelta
import re

import dateutil.parser

from curling.events.spiel import Spiel
from curling.events.draw import Draw
from curling.sites.base import BaseSite
from curling import utils


def remove_linebreaks(in_string):
    """Delete non-alphanumeric characters from in_string"""
    return re.sub(r'\n', r' ', in_string)


class Gsoc(BaseSite):
    """Scraping for The Grand Slam of Curling"""

    def parse_soup(self, soup):
        spiels = []

        target = soup.find_all("div", {"class" : "column"})
        target = target.pop()

        names = target.findAll("h5")
        schedules = target.findAll("tbody")
        for name, schedule in zip(names, schedules):
            spiel = Spiel()
            spiel.name = "GSOC " + name.text.title()
            next_tag = schedule.findNext("tr")
            while True:
                try:
                    row = next_tag.findAll("td")
                    if "odd" in next_tag.attrs["class"]:
                        draw_date = dateutil.parser.parse(row[0].text).date()
                        # Sloppy logic for determining the implicit year
                        if draw_date.month < 7 and date.today().month > 6:
                            draw_date = draw_date.replace(year=date.today().year + 1)
                    elif "even" in next_tag.attrs["class"]:
                        draw_time = dateutil.parser.parse(row[1].text).time()
                        draw_dt = utils.eastern_to_utc(datetime.combine(draw_date, draw_time))
                        draw = Draw(
                            name=remove_linebreaks(row[0].text),
                            dt=draw_dt,
                            network=remove_linebreaks(row[3].text),
                            duration=timedelta(hours=2, minutes=30))
                        spiel.add_draw(draw)
                except (KeyError, AttributeError):
                    # No more data for this spiel
                    break
                next_tag = next_tag.findNext("tr")
            spiels.append(spiel)
        return spiels
