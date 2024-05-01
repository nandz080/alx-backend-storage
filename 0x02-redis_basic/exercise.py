#!/usr/bin/env python3
"""Redis and Python exercise"""
import uuid
import redis
from typing import Union

class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method

        Args:
            data (Union[str, bytes, int, float]): Data to be stored

        Returns:
            str: string
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
