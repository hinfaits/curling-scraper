import sys
import logging

from flask import Flask, render_template, url_for, request, abort, Response

from app.events.draw import Draw
from app.events.slam import Slam
from app.sites.gsoc import Gsoc
from app.sites.tsn import Tsn
from app.scraper import Scraper
from app import config
from app import utils

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/')
def home():
    return """Stay very much woke fam<br><br>
    <a href="/data/json">/data/json</a>"""

@app.route('/data/json')
def data_csv():
    scraper = Scraper()
    scraper.attach_sites()
    scraper.scrape()
    return scraper.dump_json()
