# pylint: skip-file

import logging
from datetime import date, time, datetime, timedelta
import re

import dateutil.parser
from bs4 import BeautifulSoup

from curling.events.spiel import Spiel
from curling.events.draw import Draw
from curling.sites.base import BaseSite
from curling import utils

# url = 'http://www.tsn.ca/2017-18-curling-broadcast-schedule-1.593081'

class Tsn(BaseSite):

    def parse_soup(self, soup):
        spiels = []
        next_tag = soup.find("div", {"class":"stats-table-header"})
        while next_tag is not None:

            # Extract the event name / location
            next_tag = next_tag.find("h4")
            try:
                res = re.search("(.*) \((.*)\)", next_tag.text)
                spiel_name = res.group(1)
                spiel_loc = res.group(2)
            except AttributeError:
                spiel_name = next_tag.text
                spiel_loc = None

            spiel = Spiel(utils.header_case(spiel_name), spiel_loc)

            next_tag = next_tag.findNext("tbody")
            for row in next_tag.findAll("tr"):
                draw_info = row.findAll("td")
                draw_name = draw_info[2].text
                if "TBD" in [draw_info[0].text, draw_info[1].text]:
                    # Skip over draws with TBD date/times
                    continue
                draw_date = dateutil.parser.parse(draw_info[0].text).date()
                draw_time = dateutil.parser.parse(draw_info[1].text).time()
                draw_dt = utils.eastern_to_utc(datetime.combine(draw_date, draw_time))
                draw_network = ("TSN1/3/4/5" if draw_info[3].text == "TSN Network" else draw_info[3].text)
                draw = Draw(
                    name=draw_name,
                    dt=draw_dt,
                    network=draw_network,
                    duration=timedelta(hours=3))

                spiel.add_draw(draw)

            spiels.append(spiel)

            # Find the next block
            next_tag = next_tag.findNext("div", {"class":"stats-table-header"})
        return spiels
