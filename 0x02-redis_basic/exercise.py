#!/usr/bin/env python3
"""Module that defines a Cache class for storing and retrieving data using Redis."""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key and optionally apply a conversion function.

        Args:
            key: The Redis key to retrieve.
            fn: A callable used to convert the data type.

        Returns:
            The retrieved data, possibly converted using fn, or None if key doesn't exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 string from Redis using the given key.

        Args:
            key: The Redis key to retrieve.

        Returns:
            The retrieved string or None.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis using the given key.

        Args:
            key: The Redis key to retrieve.

        Returns:
            The retrieved integer or None.
        """
        return self.get(key, fn=int)
