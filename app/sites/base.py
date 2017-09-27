import logging
from datetime import datetime, timedelta
import json
import md5
import csv
import StringIO

try:
    from google.appengine.api import memcache
except ImportError:
    """We're not running in a GAE environment
    memcache functions will not work (NameError)"""

import dateutil

from app.events.draw import Draw
from app.events.slam import Slam

ONE_DAY = 24 * 60 * 60

class BaseSite(object):
    """docstring for BaseSite"""

    def __init__(self, url=None):
        self.url = url
        self.last_scraped = None
        self.slams = None

    def scrape(self):
        """
        Scrape the site and return
          an array of slam objects
        To be implemented by subclass
        """
        raise NotImplementedError

    def save_to_cache(self):
        key = md5.new(self.url).hexdigest()
        memcache.set(key, self.encode_json(), ONE_DAY)
        
    def load_from_cache(self):
        key = md5.new(self.url).hexdigest()
        cached = memcache.get(key)
        if cached:
            cached = self.__class__.decode_json(cached)
            self.url = cached.url
            self.last_scraped = cached.last_scraped
            self.slams = cached.slams
            return self.slams

    def get_draws(self):
        draws = []
        for slam in self.slams:
            draws = draws + slam.get_draws()
        return draws

    def encode_json(self):
        return json.dumps({
                'url': self.url,
                'last_scraped': self.last_scraped.isoformat(),
                'slams': [s.encode_json() for s in self.slams]
            })

    @classmethod
    def decode_json(cls, in_json):
        out = cls()
        j = json.loads(in_json)
        out.url = j["url"]
        out.last_scraped = dateutil.parser.parse(j["last_scraped"])
        out.slams = [Slam.decode_json(slam) for slam in j["slams"]]
        return out
