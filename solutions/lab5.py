"""Complete standalone weather wrapper. Import or run from a notebook."""

import requests
import logging
import time
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("workshop.weather")
WEATHER_TIMEOUT = 5
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WAIT_SCALE = 1  # Set 0.1 for faster practice; 1 means 1s/2s/4s.

def read_json(url, params):
    response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
    response.raise_for_status()  # Turn a bad status into a catchable error.
    return response.json()

def weather_once(city):
    places = read_json(GEOCODING_URL, {"name": city, "count": 1})
    place = places["results"][0]  # No match is caught by the wrapper.
    params = {"latitude": place["latitude"], "longitude": place["longitude"],
              "current_weather": "true"}
    weather = read_json(WEATHER_URL, params)
    temp = weather["current_weather"]["temperature"]
    if not isinstance(temp, (int, float)) or isinstance(temp, bool):
        raise ValueError("temperature must be a number")
    return {"city": city, "temp_c": temp}

def get_weather(city: str) -> dict:
    """Return current Celsius weather, or a clear error after three attempts."""
    for attempt in range(3):
        try:
            if not isinstance(city, str) or not city.strip():
                raise ValueError("city must be nonempty text")
            return weather_once(city)
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, AttributeError) as e:
            log.warning("try %d failed: %s", attempt + 1, e)
            time.sleep(WAIT_SCALE * 2 ** attempt)
    log.error("gave up on %s", city)
    return {"error": f"weather unavailable for {city}"}

get_weather_lab = get_weather
