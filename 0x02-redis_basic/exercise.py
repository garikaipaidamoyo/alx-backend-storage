import redis
import uuid
from typing import Union, Callable, List


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


def replay(func: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        func: The function for which to display the call history.
    """
    method_name = func.__qualname__
    inputs = cache._redis.lrange(f"{method_name}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_args, output_key in zip(inputs, outputs):
        input_args_str = input_args.decode()
        output_key_str = output_key.decode()
        print(f"{method_name}({input_args_str}) -> {output_key_str}")


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("foo")
    s2 = cache.store("bar")
    s3 = cache.store(42)

    replay(cache.store)
