import redis
import uuid
from functools import wraps
from typing import Callable, Optional, Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        data = self._redis.get(key)
        if data is not None and fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)

    def count_calls(fn: Callable):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            key = fn.__qualname__
            self._redis.incr(key)
            return fn(self, *args, **kwargs)
        return wrapper

    def call_history(fn: Callable):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{key}:inputs"
            outputs_key = f"{key}:outputs"
            self._redis.rpush(inputs_key, str(args))
            output = fn(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)
            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(fn: Callable):
        def wrapper(self):
            call_count = self._redis.get(fn.__qualname__)
            if call_count:
                call_count = int(call_count)
                print(f"{fn.__qualname__} was called {call_count} times:")
                inputs_key = f"{fn.__qualname__}:inputs"
                outputs_key = f"{fn.__qualname__}:outputs"
                inputs = self._redis.lrange(inputs_key, 0, call_count - 1)
                outputs = self._redis.lrange(outputs_key, 0, call_count - 1)
                for i, (inp, out) in enumerate(zip(inputs, outputs), start=1):
                    print(f"{fn.__qualname__}{inp} -> {out.decode()}")
            else:
                print(f"{fn.__qualname__} was not called.")
        return wrapper


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))

    # Task 1: Reading from Redis and recovering original type
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    # Task 4: Retrieving lists
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    cache.replay(cache.store)
