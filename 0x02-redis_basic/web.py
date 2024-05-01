#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it."""


import redis
import requests
from functools import wraps

"""redis_inst = redis.Redis()"""

def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and caches the result with an expiration time of 10 seconds."""
    # Initialize Redis connection
    r = redis.Redis()

    # Increment the access count for the URL
    r.incr(f"count:{url}")

    # Check if the page content is cached
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the HTML content of the URL
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text

        # Cache the page content with an expiration time of 10 seconds
        r.setex(url, 10, content)

        return content

    return f"Error: Unable to fetch page content from {url}"

# Test the function
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    print(get_page(url))
