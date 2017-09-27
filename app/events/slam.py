import logging
import json
from datetime import datetime, timedelta

from app.events.draw import Draw

class Slam(object):

    def __init__(self, draw_duration=timedelta(hours=1, minutes=0)):
        self.name = None
        self.location = None
        self.draw_duration = draw_duration
        self.draws = []

    def add_draw(self, draw):
        if draw.duration is None:
            draw.duration = self.draw_duration
        self.draws.append(draw)

    def start_date(self):
        raise NotImplementedError

    def end_date(self):
        raise NotImplementedError

    def get_draws(self):
        ret = []
        for draw in self.draws:
            draw_info = draw.properties()
            draw_info["summary"] = " - ".join([self.name, draw_info["summary"]])
            ret.append(draw_info)
        return ret

    def encode_json(self):
        return json.dumps({
            'name': self.name,
            'location': self.location,
            'draw_duration': self.draw_duration.total_seconds(),
            'draws': [d.encode_json() for d in self.draws],
            })

    @classmethod
    def decode_json(cls, in_json):
        out = cls()
        j = json.loads(in_json)
        out.name = j["name"]
        out.location = j["location"]
        out.draw_duration = timedelta(seconds=j["draw_duration"])
        out.draws = [Draw.decode_json(draw) for draw in j["draws"]]
        return out
