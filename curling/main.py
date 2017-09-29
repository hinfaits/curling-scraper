import sys
import logging

from flask import Flask

from curling.scraper import Scraper
# from curling import config

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
