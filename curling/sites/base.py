import logging
from datetime import datetime
import json
import md5

try:
    from google.appengine.api import memcache
    GAE = True
except ImportError:
    """We're not running in a GAE environment and
    memcache functions will not work (NameError)"""
    GAE = False

from bs4 import BeautifulSoup
import dateutil.parser

from curling.events.spiel import Spiel
# from curling.events.draw import Draw
from curling import utils

ONE_DAY = 24 * 60 * 60

class BaseSite(object):

    def __init__(self, url=None):
        self.url = url
        self.last_scraped = None
        self.spiels = None

    def parse_soup(self, soup):
        raise NotImplementedError

    def scrape(self, cache=True):
        html = utils.get_url(self.url)
        soup = BeautifulSoup(html, "html.parser")

        self.spiels = self.parse_soup(soup)
        self.last_scraped = datetime.utcnow()
        if cache:
            self.save_to_cache()

        return self.spiels

    def _key(self):
        return md5.new(self.url).hexdigest()

    def save_to_cache(self):
        if GAE:
            memcache.set(self._key(), self.serialize(), ONE_DAY)

    def load_from_cache(self):
        if not GAE:
            return
        cached = memcache.get(self._key())
        if cached:
            cached = self.__class__.deserialize(cached)
            self.url = cached.url
            self.last_scraped = cached.last_scraped
            self.spiels = cached.spiels
            return self.spiels

    def get_draws(self):
        draws = []
        for spiel in self.spiels:
            draws = draws + spiel.get_draws()
        return draws

    def serialize(self):
        return json.dumps({
            'url': self.url,
            'last_scraped': self.last_scraped.isoformat(),
            'spiels': [s.serialize() for s in self.spiels]})

    @classmethod
    def deserialize(cls, in_json):
        out = cls()
        j = json.loads(in_json)
        out.url = j["url"]
        out.last_scraped = dateutil.parser.parse(j["last_scraped"])
        out.spiels = [Spiel.deserialize(spiel) for spiel in j["spiels"]]
        return out
