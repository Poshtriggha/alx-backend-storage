#!/usr/bin/env python3

"""
Cache module provides a class to store data in Redis cache.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class provides methods to store data in Redis cache.
    """
    def __init__(self) -> None:
        """
        Initialize a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used for storing the data.
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

