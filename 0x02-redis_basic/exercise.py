#!/usr/bin/env python3
"""Module that defines a Cache class for storing data in Redis."""

import redis
import uuid
from typing import Union


class Cache:
    """Cache class to store and retrieve data from Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to store. Can be str, bytes, int, or float.

        Returns:
            The generated Redis key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
