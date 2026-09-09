import os
import random
import time

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, max_retries: int = 3) -> dict:
    """Fetch weather data with exponential backoff and jitter."""

    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is missing in .env")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=30,
            )

            # Retry only temporary failures and rate limits
            if response.status_code in (429, 500, 502, 503, 504):
                if attempt == max_retries:
                    response.raise_for_status()

                delay = (2 ** attempt) + random.uniform(0, 1)

                print(
                    f"Temporary API failure "
                    f"({response.status_code}). "
                    f"Retrying in {delay:.2f} seconds..."
                )

                time.sleep(delay)
                continue

            # Handle permanent errors immediately
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            if attempt == max_retries:
                raise

            delay = (2 ** attempt) + random.uniform(0, 1)

            print(
                f"Request timed out. "
                f"Retrying in {delay:.2f} seconds..."
            )

            time.sleep(delay)

        except requests.exceptions.ConnectionError:
            if attempt == max_retries:
                raise

            delay = (2 ** attempt) + random.uniform(0, 1)

            print(
                f"Connection error. "
                f"Retrying in {delay:.2f} seconds..."
            )

            time.sleep(delay)

    raise RuntimeError("API request failed after all retries")