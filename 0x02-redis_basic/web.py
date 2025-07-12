#!/usr/bin/env python3
"""Module for caching web pages and tracking access counts."""

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator that counts how many times a URL was accessed.
    Increments Redis key: count:{url}
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator that caches the result of a URL fetch for 10 seconds.
    Uses Redis key: {url}
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        cached = r.get(url)
        if cached:
            return cached.decode('utf-8')
        result = method(url)
        r.setex(url, 10, result)
        return result
    return wrapper


@count_access
@cache_result
def get_page(url: str) -> str:
    """
    Fetches HTML content of a URL, with access count tracking and 10-second caching.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
