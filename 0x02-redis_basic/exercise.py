#!/usr/bin/env python3
"""A class Cache class. It has an init method that stores
an instance of the Redis client as a private variable"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """A decorator that takes a single method Callable argument
     and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """increments the count for that key every time the
        method is called and returns the value returned by the
        original method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """A decorator to store the history of inputs and
    outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """to retrieve the output. Store the output using rpush in the
        "...:outputs" list, then return the output"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper

def replay(fn: Callable):
    """Displays the history of calls of a particular function"""
    rd = redis.Redis()
    func_name = fn.__qualname__
    num_calls = rd.get(func_name)
    try:
        num_calls = num_calls.decode('utf-8')
    except Exception:
        num_calls = 0
    print(f'{func_name} was called {num_calls} times:')

    inpts = rd.lrange(func_name + ":inputs", 0, -1)
    otpts = rd.lrange(func_name + ":outputs", 0, -1)

    for i, o in zip(inpts, otpts):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{func_name}(*{i}) -> {o}')

class Cache:
    """a class that has all the functions required"""
    def __init__(self):
        self._redis = redis.Redis()
        self.flushdb()

    def flushdb(self):
        """flushes the redis database"""
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores the input data in Redis using randomly"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """take a key string argument and an optional
        Callable argument named fn"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """parametrizes cache.get with the correct conversion function"""
        variable = self._redis.get(key)
        return variable.decode("UTF-8")

    def get_int(self, key: str) -> int:
        """parametrizes cache.get with the correct conversion function"""
        variable = self._redis.get(key)
        try:
            variable = int(variable.decode("UTF-8"))
        except Exception:
            variable = 0
        return variable
