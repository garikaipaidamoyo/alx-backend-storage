import redis
import uuid
from typing import Union, Callable


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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and
    outputs for a function in Redis.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Get the qualified name of the method
        method_name = method.__qualname__

        # Convert input arguments to a string and store in Redis
        input_key = f"{method_name}:inputs"
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        result = method(self, *args, **kwargs)

        # Store the output in Redis
        output_key = f"{method_name}:outputs"
        self._redis.rpush(output_key, result)

        return result

    return wrapper


if __name__ == "__main__":
    cache = Cache()

    # Decorate Cache.store with call_history
    Cache.store = call_history(Cache.store)

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(
        f"{cache.store.__qualname__}:inputs", 0, -1
    )
    outputs = cache._redis.lrange(
        f"{cache.store.__qualname__}:outputs", 0, -1
    )

    print("inputs:", [input.decode() for input in inputs])
    print("outputs:", [output.decode() for output in outputs])
