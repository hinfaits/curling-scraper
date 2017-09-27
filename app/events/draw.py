import logging
import json
from datetime import datetime, timedelta
import re

import dateutil

from app import config


def str_cleanse(in_string):
    """Delete non-alphanumeric characters from in_string"""
    return re.sub(r'[^A-Za-z0-9]', r'', in_string)


class Draw(object):

    def __init__(self):
        self.name = None
        self.datetime = None
        self.network = None
        self.duration = None

    def properties(self):
        summary = self.name
        description = "On " + self.network
        dtstart = self.datetime.isoformat()
        dtend = (self.datetime + self.duration).isoformat()
        uid = "".join([str_cleanse(summary), dtstart, "@", config.host])
        return {
            'summary': summary,
            'description': description,
            'dtstart': dtstart,
            'dtend': dtend,
            'dtstamp': datetime.now().isoformat(),
            'uid': uid,
        }

    def encode_json(self):
        return json.dumps({
            'name': self.name,
            'datetime': self.datetime.isoformat(),
            'duration': self.duration.total_seconds(),
            'network': self.network,
        })

    @classmethod
    def decode_json(cls, in_json):
        out = cls()
        j = json.loads(in_json)
        out.name = j["name"]
        out.network = j["network"]
        out.duration = timedelta(seconds=j["duration"])
        out.datetime = dateutil.parser.parse(j["datetime"])
        return out
