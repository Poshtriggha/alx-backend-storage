#!/usr/bin/env python3
"""This function implements an expiring web cache and tracker"""

import requests
import redis
import time
from functools import wraps

store = redis.Redis()

def cache_with_expiration(method):
    """A decorator that counts the times a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        # Generate cache key
        cache_key = "cached:" + url
        # Check if the data is already cached
        cached_data = store.get(cache_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # If not cached, increment count key and cache the data
        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)  # Increment count of URL access
        store.set(cache_key, html)  # Cache the HTML content
        store.expire(cache_key, 10)  # Set expiration time (10 seconds)
        return html
    return wrapper

@cache_with_expiration
def get_page(url: str) -> str:
    """Returns HTML content from a URL"""
    re = requests.get(url)
    return re.text
