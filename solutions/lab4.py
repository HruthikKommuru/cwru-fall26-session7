"""Three bounded attempts with repeatable, testable behavior."""
import logging
import time
import requests
from starter.flaky_api import flaky_api

log = logging.getLogger("workshop.retries")


def retry_flaky(wait_scale=0.1):
    for attempt in range(3):
        try:
            return flaky_api()
        except requests.Timeout:
            log.warning("retry %d for %s", attempt + 1, "pretend API")
            time.sleep(wait_scale * 2 ** attempt)
    log.error("gave up on %s", "pretend API")
    return {"error": "gave up after 3 tries"}
