#!/usr/bin/env python3
"""Module that defines a Cache class for storing and retrieving data using Redis with tracking."""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Uses Redis to store the count using method's qualified name.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments call count and calls original method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method.

    Inputs are stored in '<method_name>:inputs' list,
    Outputs are stored in '<method_name>:outputs' list.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper that logs inputs and outputs."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Save input as string
        self._redis.rpush(input_key, str(args))

        # Call original method
        result = method(self, *args, **kwargs)

        # Save output
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper


class Cache:
    """Cache class to store and retrieve data from Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
