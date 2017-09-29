import logging
from datetime import timedelta

try:
    from google.appengine.api import urlfetch
except ImportError:
    import urllib2

# import curling.config


def get_url(url):
    try:
        result = urlfetch.fetch(url)
        return result.content
    except NameError:
        res = urllib2.urlopen(url)
        return res.read()

def is_dst(dt):
    month = dt.month
    if month < 3 or month > 11:
        return False
    elif month > 3 or month < 11:
        return True
    else:
        previous_sunday = dt.day - dt.weekday()
        if month == 3:
            return bool(previous_sunday >= 8)
        elif month == 11:
            return bool(previous_sunday < 0)


def eastern_to_utc(dt):
    """Convert naive dt object from eastern to utc
    Will detect and correct for DST"""
    if is_dst(dt):
        td = timedelta(hours=4)
    else:
        td = timedelta(hours=5)
    return dt + td

    # This is the (more elegant) pytz way of doing it which doesn't work on GAE
    eastern = pytz.timezone("America/New_York")
    est_dt = eastern.localize(dt)
    return est_dt.astimezone(pytz.utc)
