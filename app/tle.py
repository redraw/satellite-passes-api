import os
import json
import logging
import requests

from utils import cache

CELESTRAK_API_TLE = "https://celestrak.com/NORAD/elements/gp.php"
CACHE_TIMEOUT = 12 * 60 * 60 # 12 hours

logger = logging.getLogger('api.tle')
session = requests.Session()


class TLENotFound(Exception):
    pass


def get_tle(norad_id):
    """Get latest TLE from API"""
    cache_key = f"tle:{norad_id}"
    tle = cache.get(cache_key)

    if tle:
        logger.info(f"Cache TLE HIT norad={norad_id}")
        return tle.split("\n")

    response = session.get(CELESTRAK_API_TLE, params={
        "CATNR": norad_id,
        "FORMAT": "TLE"
    })

    tle = response.text

    if tle == "No GP data found":
        raise TLENotFound

    logger.info(f"Cache TLE MISS, saving norad={norad_id}")
    cache.set(cache_key, tle, CACHE_TIMEOUT)

    return tle.split("\n")
