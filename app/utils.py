import math
import time
from hashlib import md5
import redis

import settings

cache = redis.Redis.from_url(settings.REDIS_URL)


def get_cache_key(*args, prefix=""):
    payload = ":".join(str(arg) for arg in args).encode('utf8')
    return f"{prefix}:{md5(payload).hexdigest()}"


def az_to_octant(azimuth):
    octants = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = (int(azimuth) / 360) * 8
    return octants[round(idx) % 8]


def filter_next_passes(passes):
    return [
        p for p in passes
        if p["set"]["utc_timestamp"] > time.time()
    ]
