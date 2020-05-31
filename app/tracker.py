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
        self.eph = skyfield_load("de421.bsp")
        self.observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
        self.timescale = skyfield_load.timescale()
        self.sun = self.eph["sun"]
        self.horizon = horizon
        tle = get_tle(norad_id)
        self.satellite = EarthSatellite(tle["line1"], tle["line2"], tle["name"], self.timescale)

    def next_passes(self, days=7, visible_only=False):
        passes = []
        now = self.timescale.now()

        t0, t1 = now, self.timescale.utc(
            now.utc_datetime() + timedelta(days=days)
        )

        times, events = self.satellite.find_events(
            self.observer, t0, t1, altitude_degrees=self.horizon
        )

        for pass_times, pass_events in zip(chunked(times, 3), chunked(events, 3)):
            full_pass = self.serialize_pass(pass_times, pass_events)
            full_pass["visible"] = any(event["visible"] for event in full_pass.values())
            passes.append(full_pass)

        if visible_only:
            passes = [p for p in passes if p["visible"]]

        return passes

    def serialize_pass(self, pass_times, pass_events):
        full_pass = {}
        observer_barycenter = self.eph["earth"] + self.observer

        for time, event_type in zip(pass_times, pass_events):
            geometric_sat = (self.satellite - self.observer).at(time)
            geometric_sun = (self.eph["sun"] - observer_barycenter).at(time)

            sat_alt, sat_az, sat_d = geometric_sat.altaz()
            sun_alt, sun_az, sun_d = geometric_sun.altaz()

            is_sunlit = geometric_sat.is_sunlit(self.eph)
            event = ('rise', 'culmination', 'set')[event_type]

            full_pass[event] = {
                "alt": f"{sat_alt.degrees:.2f}",
                "az": f"{sat_az.degrees:.2f}",
                "az_octant": az_to_octant(sat_az.degrees),
                "utc_datetime": str(time.utc_datetime()),
                "utc_timestamp": int(time.utc_datetime().timestamp()),
                "is_sunlit": bool(is_sunlit),
                "visible": -18 <= int(sun_alt.degrees) <= -6 and bool(is_sunlit)
            }

        return full_pass
