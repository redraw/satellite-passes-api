import redis
import math

import settings


cache = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def az_to_octant(azimuth):
    octants = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = math.floor(azimuth) / (2*math.pi/8)
    return octants[round(idx) % 8]
