import requests
import redis
from functools import wraps
import time

# Initialize the Redis client
redis_client = redis.Redis()


def track_access(url):
    """A decorator to track URL access count."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count_key = f"count:{url}"
            # Increment the access count
            redis_client.incr(count_key)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_page(url, expiration=10):
    """A decorator to cache a page with a specified expiration time."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"cache:{url}"
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return cached_data.decode("utf-8")
            else:
                content = func(*args, **kwargs)
                redis_client.setex(cache_key, expiration, content)
                return content
        return wrapper
    return decorator


@track_access
@cache_page
def get_page(url):
    """Fetch the web page's HTML content and return it."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch URL - {url}"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/example.com"
    html_content = get_page(url)
    access_count = redis_client.get(f"count:{url}")
    print(f"URL Access Count: {access_count.decode()}")
    print(f"HTML Content:\n{html_content}")
