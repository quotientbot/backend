import typing as T
import time
from enum import Enum


class CacheName(Enum):
    """Cache name enum"""

    GUILD = "guild"
    USER = "user"


class CacheManager:
    _caches = {"guild": {}, "user": {}}
    ttl = 60  # default ttl (in seconds)

    @classmethod
    def get(cls, cache_name: CacheName, key: str):
        cache = cls._caches[cache_name.value]
        item = cache.get(key, None)

        if item and item["expiry"] > time.time():
            return item["value"]

        return None

    @classmethod
    def set(cls, cache_name: CacheName, key: str, value: T.Any, ttl=None):
        cache = cls._caches.get(cache_name.value, {})
        ttl = ttl or cls.ttl

        item = {"value": value, "expiry": time.time() + ttl}
        cache[key] = item

        cls._caches[cache_name.value] = cache
