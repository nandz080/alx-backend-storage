#!/usr/bin/env python3
"""Redis and Python exercise"""
import uuid
import redis
from typing import Union, Callable
from functools import wraps
import redis

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

def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """saves the input and output of each function in redis
        """
        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(inputs_key, str(args))
        self._redis.rpush(outputs_key, str(output))

        return output

    return wrapper

def replay(fn: Callable):
    """Display the history of calls of a particular function"""
    redis_inst = redis.Redis()
    funcName = fn.__qualname__
    calls = redis_inst.get(funcName)
    try:
        calls = calls.decode('utf-8')
    except Exception:
        calls = 0
    print(f'{funcName} was called {calls} times:')

    inputs = redis_inst.lrange(funcName + ":inputs", 0, -1)
    outputs = redis_inst.lrange(funcName + ":outputs", 0, -1)

    for ins, oots in zip(inputs, outputs):
        try:
            ins = ins.decode('utf-8')
        except Exception:
            ins = ""
        try:
            outs = outs.decode('utf-8')
        except Exception:
            outs = ""

        print(f'{funcName}(*{ins}) -> {outs}')

class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history

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

# Call the store method multiple times
cache.store("foo")
cache.store("bar")
cache.store(42)

# Use the replay function to display the history of calls of the store method
replay(cache.store)
