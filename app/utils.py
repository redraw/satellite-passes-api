import math
import time
from hashlib import md5
import redis

import settings

cache = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_cache_key(*args, prefix=""):
    payload = ":".join(str(arg) for arg in args).encode('utf8')
    return f"{prefix}:{md5(payload).hexdigest()}"


def az_to_octant(azimuth):
    octants = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = (int(azimuth) / 360) * len(octants)
    return octants[round(idx) % len(octants)]


def filter_next_passes(passes):
    current_time = time.time()
    return [
        p for p in passes
        if any(
            p[event]["utc_timestamp"] > current_time
            for event in ("set", "culmination", "rise")
            if event in p
        )
    ]
