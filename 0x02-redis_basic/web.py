#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it."""


import redis
import requests
from functools import wraps

redis_inst = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_content = redis_inst.get(key)
        if cached_content:
            return cached_content.decode("utf-8")

            # Get new content and update cache
        count = "count:" + url
        content = method(url)

        redis_inst.incr(count)
        redis_inst.set(key, content, ex=10)
        redis_inst.expire(key, 10)
        return content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    outputs = requests.get(url)
    return outputs.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
