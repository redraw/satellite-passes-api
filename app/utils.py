import math
from hashlib import md5
import redis

import settings

cache = redis.Redis.from_url(settings.REDIS_URL)


def get_cache_key(*args, prefix=""):
    payload = "".join(str(arg) for arg in args).encode('utf8')
    return f"{prefix}:{md5(payload).hexdigest()}"


def az_to_octant(azimuth):
    octants = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = math.floor(azimuth) / (2*math.pi/8)
    return octants[round(idx) % 8]
