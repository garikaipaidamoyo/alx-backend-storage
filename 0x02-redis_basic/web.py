#!/usr/bin/env python3
"""
web.py: A module to implement a
web page caching and tracking function.
"""

import requests
import redis

# Initialize a Redis client
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL, cache the result
    with a 10-second expiration time, and track the number
    of accesses to the URL.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    # Define the Redis key for tracking the access count
    count_key = f"count:{url}"

    # Increment the access count for the URL
    access_count = redis_client.incr(count_key)

    # Check if the URL content is cached
    cached_content = redis_client.get(url)

    if cached_content is not None:
        return cached_content.decode("utf-8")

    # If not cached, fetch the web page content
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text

        # Cache the web page content with a 10-second expiration
        redis_client.setex(url, 10, page_content)

        return page_content

    # If the response status is not 200, return an empty string
    return ""


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/" \
          "http://www.google.com"
    content = get_page(url)
    print(content)
