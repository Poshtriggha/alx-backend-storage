#!/usr/bin/env python3
"""
Cache module
"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    """
    Cache class to store data in Redis
    """
    def __init__(self) -> None:
        """
        Initialize Cache class with Redis client
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store history of inputs and outputs for a function
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:outputs".format(method.__qualname__)
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, output)
            return output
        return wrapper

    @staticmethod
    def replay(method: Callable) -> None:
        """
        Display history of calls for a particular function
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        inputs = Cache._redis.lrange(input_key, 0, -1)
        outputs = Cache._redis.lrange(output_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for input_args, output in zip(inputs, outputs):
            print(f"{method.__qualname__}{eval(input_args)} -> {output}")

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    Cache.replay(cache.store)
