#!/usr/bin/env python3
"""Redis and Python exercise"""
import uuid
import redis
from typing import Union, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method Callable args
    and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """INCR the count for that key every time the method
        is called and returns the value returned by the original method """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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
