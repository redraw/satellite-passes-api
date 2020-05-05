import os
import json
import ephem
import redis
import logging
import requests

from datetime import datetime
from math import degrees
from utils import az_to_octant
from collections import namedtuple

REDIS_URL = os.getenv("FLY_REDIS_CACHE_URL", "redis://localhost")
NASA_TLE_API_KEY = os.getenv("NASA_TLE_API_KEY")
NASA_TLE_API_URL = "https://data.ivanstanojevic.me/api/tle"

cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)

EphemPass = namedtuple('EphemPass', [
    'rise_time',
    'rise_az',
    'max_alt_time',
    'max_alt',
    'set_time',
    'set_az'
])


class SatTracker:
    def __init__(self, lat, lon, horizon='10', norad_id=25544):
        self.observer = ephem.Observer()
        self.observer.lat = lat
        self.observer.lon = lon

        # disable atmospheric reflection
        self.observer.pressure = 0
        self.observer.horizon = horizon

        self.sun = ephem.Sun()

        tle = self.get_tle(norad_id)
        self.satellite = ephem.readtle(tle["name"], tle["line1"], tle["line2"])

    def get_tle(self, norad_id):
        """Get latest TLE from SpaceTrack API"""
        cache_key = f"tle:{norad_id}"

        tle = cache.get(cache_key)
        if tle:
            print(f"[cache HIT] fetched tle norad={norad_id}")
            return json.loads(tle)

        url = f"{NASA_TLE_API_URL}/{norad_id}"
        assert NASA_TLE_API_KEY is not None
        response = requests.get(url, {"api_key": NASA_TLE_API_KEY})
        tle = response.json()

        print(f"[cache MISS] saving tle norad={norad_id} ttl=6h")
        cache.set(cache_key, json.dumps(tle), 6 * 60 * 60)

        return tle

    def get_next_passes(self, n=15, visible_only=False):
        passes = []

        self.observer.date = datetime.utcnow()

        computed_pass = self.yield_next_pass()

        for _ in range(n):
            p = next(computed_pass)
            passes.append(p)

        if visible_only:
            return filter(lambda p: p['visible'], passes)

        return passes

    def yield_next_pass(self):
        """Yield next pass for observer/satellite"""

        while True:
            try:
                next_pass = self.observer.next_pass(self.satellite)
            except ephem.CircumpolarError:
                # no passes for you!
                logger.info(
                    "Tried to calculate passes for circumpolar sat"
                    "@ {}".format(self.observer)
                )
                raise

            _pass = EphemPass(*next_pass)

            yield self.compute_pass(_pass)

            # advance 1 hour after pass to compute next pass
            self.observer.date = _pass.set_time + (60 * ephem.minute)

    def compute_pass(self, _pass):
        """
        Computes a pass across the observer's time.
        Returns start/max/end times and if it's probably visible.
        """

        visible = False
        passing_time = _pass.rise_time

        while passing_time < _pass.set_time:
            passing_time += ephem.second
            self.observer.date = passing_time

            self.sun.compute(self.observer)
            self.satellite.compute(self.observer)

            if (
                not self.satellite.eclipsed and
                -18 < degrees(self.sun.alt) < -6
            ):
                visible = True
                break

        # set highest azimuth
        self.observer.date = _pass.max_alt_time
        self.satellite.compute(self.observer)
        highest_az = self.satellite.az

        # TODO: add approx magnitude

        return {
            'start': {
                'datetime': _pass.rise_time.datetime(),
                'timestamp': int(_pass.rise_time.datetime().timestamp()),
                'alt': degrees(self.observer.horizon),
                'az': az_to_octant(_pass.rise_az)
            },
            'highest': {
                'datetime': _pass.max_alt_time.datetime(),
                'timestamp': int(_pass.max_alt_time.datetime().timestamp()),
                'alt': degrees(_pass.max_alt),
                'az': az_to_octant(highest_az)
            },
            'end': {
                'datetime': _pass.set_time.datetime(),
                'timestamp': int(_pass.set_time.datetime().timestamp()),
                'alt': degrees(self.observer.horizon),
                'az': az_to_octant(_pass.set_az)
            },
            'visible': visible
        }


class CelesTrak(object):
    FEED_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"

    def __init__(self):
        self.session = requests.Session()

    def update(self):
        r = self.session.get(TLE.FEED_URL)
        lines = [line.strip() for line in r.text.split('\n') if line]

        satellites = []

        for i in range(0, len(lines), 3):
            satellites.append(lines[i:i+3])

        with open('tle.json', 'w') as f:
            json.dump(satellites, f, indent=4)
