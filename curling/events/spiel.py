# pylint: disable=import-error

import logging
import json
# from datetime import datetime, timedelta

from curling.events.draw import Draw

class Spiel(object):

    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        self.draws = []

    def add_draw(self, draw):
        self.draws.append(draw)

    def start_date(self):
        raise NotImplementedError

    def end_date(self):
        raise NotImplementedError

    def get_draws(self):
        ret = []
        for draw in self.draws:
            draw_info = draw.ical_attrs()
            # Append the spiel name to the draw name
            draw_info["summary"] = " - ".join([self.name, draw_info["summary"]])
            ret.append(draw_info)
        return ret

    def serialize(self):
        return json.dumps({
            'name': self.name,
            'location': self.location,
            'draws': [d.serialize() for d in self.draws],
            })

    @classmethod
    def deserialize(cls, in_json):
        out = cls()
        j = json.loads(in_json)
        out.name = j["name"]
        out.location = j["location"]
        out.draws = [Draw.deserialize(draw) for draw in j["draws"]]
        return out
