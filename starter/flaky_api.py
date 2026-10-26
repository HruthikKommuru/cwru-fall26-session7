"""A pretend API that needs no internet connection."""
import random
import requests


def flaky_api():
    """Time out about half the time; otherwise return a small dictionary."""
    if random.random() < 0.5:
        raise requests.Timeout("Our pretend API took too long")
    return {"status": "ok"}
