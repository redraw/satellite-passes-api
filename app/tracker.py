import os
import json
import logging
from datetime import datetime, timedelta
from more_itertools import chunked
from skyfield.api import EarthSatellite, Topos
from skyfield.api import load as skyfield_load

from math import degrees
from tle import get_tle
from utils import cache, az_to_octant

logger = logging.getLogger(__name__)


class SatTracker:
    def __init__(self, lat, lon, norad_id=None, horizon=10.0):
        tle = get_tle(norad_id)
        self.horizon = horizon
        self.timescale = skyfield_load.timescale(builtin=True)
        self.observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
        self.satellite = EarthSatellite(tle["line1"], tle["line2"], tle["name"], self.timescale)

    def next_passes(self, days=7):
        passes = []
        now = self.timescale.now()

        t0, t1 = now, self.timescale.utc(
            now.utc_datetime() + timedelta(days=days)
        )

        times, events = self.satellite.find_events(
            self.observer, t0, t1, altitude_degrees=self.horizon
        )

        for pass_times, pass_events in zip(chunked(times, 3), chunked(events, 3)): 
            full_pass = self.build_full_pass(pass_times, pass_events)
            passes.append(full_pass)

        return passes

    def build_full_pass(self, pass_times, pass_events):
        full_pass = {}
        for time, event_type in zip(pass_times, pass_events): 
            alt, az, d = (self.satellite - self.observer).at(time).altaz()
            event = ('rise', 'culmination', 'set')[event_type]
            full_pass[event] = {
                "alt": f"{alt.degrees:.2f}", 
                "az": f"{az.degrees:.2f}", 
                "utc_datetime": time.utc_datetime()
            }
        return full_pass