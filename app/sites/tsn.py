import logging
from datetime import datetime
import md5

from bs4 import BeautifulSoup

from app.sites.base import BaseSite
from app import utils

url = 'http://www.tsn.ca/2017-18-curling-broadcast-schedule-1.593081'

class Tsn(BaseSite):

    # def __init__(self):
    #     super(self.__class__, self).__init__()

    def scrape(self):
        html = utils.url_open(self.url)
        soup = BeautifulSoup(html, "html.parser")

        soup.find_all("div", { "class" : "stats-table" })
