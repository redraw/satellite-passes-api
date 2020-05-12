import os
import json
import logging
import requests

from utils import cache


NASA_TLE_API_URL = "https://data.ivanstanojevic.me/api/tle"
NASA_TLE_API_KEY = os.getenv("NASA_TLE_API_KEY")
CACHE_TIMEOUT = 12 * 60 * 60 # 12 hours

logger = logging.getLogger(__name__)
session = requests.Session()


def get_tle(norad_id):
    """Get latest TLE from API"""
    cache_key = f"tle:{norad_id}"

    tle = cache.get(cache_key)
    if tle:
        logger.info(f"cache [HIT] fetched tle norad={norad_id}")
        return json.loads(tle)

    url = f"{NASA_TLE_API_URL}/{norad_id}"
    assert NASA_TLE_API_KEY is not None, "Missing NASA TLE API Key"
    response = requests.get(url, {"api_key": NASA_TLE_API_KEY})
    tle = response.json()

    logger.info(f"cache [MISS] saving tle norad={norad_id}")
    cache.set(cache_key, json.dumps(tle), CACHE_TIMEOUT)

    return tle
