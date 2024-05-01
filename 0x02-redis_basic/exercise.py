#!/usr/bin/env python3
"""Redis and Python exercise"""
import uuid
import redis
from typing import Union, Callable

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

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """ Get data from redis and transform it to its python type """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Transform a redis type variable to a str python type """
        parm = self._redis.get(key)
        return parm.decode("UTF-8")

    def get_int(self, key: str) -> int:
        """ Transform a redis type variable to a str python type """
        parm = self._redis.get(key)
        try:
            parm = int(parm.decode("UTF-8"))
        except Exception:
            parm = 0
        return parm

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
