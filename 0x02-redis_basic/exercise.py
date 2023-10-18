#!/usr/bin/env python3
"""
Cache module
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for working with Redis
    """

    def __init__(self):
        """
        Initialize the Cache instance with a
        Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data: The data to be stored in Redis (str, bytes, int, or float).

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
