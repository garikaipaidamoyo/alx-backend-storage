import redis
import uuid
from typing import Union, Callable, Optional
import functools


class Cache:
    """
    Cache class for working with Redis
    """

    def __init__(self):
        """
        Initialize the Cache instance with a Redis client and
        flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float] = None) -> str:
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


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts how many times a method is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        count = self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result
    return wrapper


if __name__ == "__main__":
    cache = Cache()

    @count_calls
    def decorated_store(data: Union[str, bytes, int, float] = None) -> str:
        return cache.store(data)

    cache.store(b"first")
    print(
            decorated_store.__qualname__,
            cache.get(decorated_store.__qualname__)
    )

    cache.store(b"second")
    cache.store(b"third")
    print(
            decorated_store.__qualname__,
            cache.get(decorated_store.__qualname__)
    )
