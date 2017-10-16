# pylint: disable=invalid-name
# pylint: disable=import-error

import sys
import logging

from flask import Flask

from curling import config
from curling.scraper import Scraper

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/')
def home():
    # pylint: disable=line-too-long
    return """<a href="https://github.com/hinfaits/curling-scraper">//github.com/hinfaits/curling-scraper</a><br><br>
    <a href="/data/json">/data/json</a>"""

@app.route('/data/json')
def data_csv():
    scraper = Scraper()
    for url in config.site_urls:
        scraper.attach_site(url)
    scraper.scrape()
    return scraper.dump_json()

if __name__ == "__main__":
    pass
