import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis by key and
        optionally apply a conversion function.

        Args:
            key: The key used to retrieve data from Redis.
            fn: A callable function to convert the retrieved data (optional).

        Returns:
            Union[str, bytes, int, float]:
            The retrieved data with an optional conversion.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes]:
        """
        Retrieve data from Redis as a string.

        Args:
            key: The key used to retrieve data from Redis.

        Returns:
            Union[str, bytes]: The retrieved data as a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, bytes]:
        """
        Retrieve data from Redis as an integer.

        Args:
            key: The key used to retrieve data from Redis.

        Returns:
            Union[int, bytes]: The retrieved data as an integer.
        """
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
