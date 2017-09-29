import logging
from datetime import date, time, datetime, timedelta

import dateutil.parser
from bs4 import BeautifulSoup

from curling.events.spiel import Spiel
from curling.events.draw import Draw
from curling.sites.base import BaseSite
from curling import utils

# url = 'http://www.tsn.ca/2017-18-curling-broadcast-schedule-1.593081'

class Tsn(BaseSite):

    def parse_soup(self, soup):
        pass
