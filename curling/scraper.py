# pylint: disable=import-error

import logging
from urlparse import urlparse
import json

from curling.sites.gsoc import Gsoc
from curling.sites.tsn import Tsn


class Scraper(object):

    def __init__(self):
        self.sites = []

    @staticmethod
    def init_site_from_url(url):
        """Factory method for getting a Site class from URL"""
        parsed = urlparse(url)
        if 'tsn.ca' in parsed.netloc:
            return Tsn(url)
        elif 'thegrandslamofcurling.com' in parsed.netloc:
            return Gsoc(url)
        else:
            return None

    def attach_site(self, url):
        self.sites.append(self.init_site_from_url(url))

    def scrape(self, flush_cache=False):
        for site in self.sites:
            site.load_from_cache()
            if site.last_scraped and not flush_cache:
                # Loaded from cache
                pass
            else:
                site.scrape()

    def get_draws(self):
        draws = []
        for site in self.sites:
            draws = draws + site.get_draws()
        return draws

    def dump_json(self):
        return json.dumps(self.get_draws())
