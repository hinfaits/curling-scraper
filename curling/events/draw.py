# pylint: disable=import-error

import logging
import json
from datetime import datetime, timedelta
import re

import dateutil

from curling import config


def str_cleanse(in_string):
    """Remove all nonalphanumeric characters from `in_string`"""
    return re.sub(r'[^A-Za-z0-9]', r'', in_string)


class Draw(object):

    def __init__(self, name=None, dt=None, network=None, duration=timedelta(hours=1)):
        self.name = name
        self.datetime = dt
        self.network = network
        self.duration = duration
        self.stamp = datetime.utcnow() # Used for the dtstamp ical attribute

    def ical_attrs(self):
        """Get all of the attrs in `self` as a dict"""
        summary = self.name
        description = "On " + self.network
        dtstart = self.datetime.isoformat()
        dtend = (self.datetime + self.duration).isoformat()
        dtstamp = self.stamp.isoformat()
        uid = "".join([str_cleanse(summary), dtstart, "@", config.hostname])
        return {
            'summary': summary,
            'description': description,
            'dtstart': dtstart,
            'dtend': dtend,
            'dtstamp': dtstamp,
            'uid': uid,
        }

    def serialize(self):
        """Get all of the attrs in `self` as a json str"""
        return json.dumps({
            'name': self.name,
            'datetime': self.datetime.isoformat(),
            'duration': self.duration.total_seconds(),
            'network': self.network,
            'stamp': self.stamp.isoformat(),
        })

    @classmethod
    def deserialize(cls, in_json):
        """Get an instance of `Draw` from a json str"""
        out = cls()
        j = json.loads(in_json)
        out.name = j["name"]
        out.network = j["network"]
        out.duration = timedelta(seconds=j["duration"])
        out.datetime = dateutil.parser.parse(j["datetime"])
        out.stamp = dateutil.parser.parse(j["stamp"])
        return out
