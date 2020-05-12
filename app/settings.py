import os


REDIS_URL = os.getenv("FLY_REDIS_CACHE_URL", "redis://localhost")
