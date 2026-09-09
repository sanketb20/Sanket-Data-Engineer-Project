from api_client import get_weather
from checkpoint import load_checkpoint, save_checkpoint

import requests
import json
from pathlib import Path
from datetime import datetime


def main():
    city = input("Enter city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    checkpoint = load_checkpoint()

    if checkpoint:
        print("\nPrevious successful ingestion:")
        print(f"City: {checkpoint.get('last_successful_city')}")
        print(f"File: {checkpoint.get('last_successful_file')}")
        print(
            f"Fetched at: "
            f"{checkpoint.get('last_successful_fetch_utc')}"
        )
    else:
        print("\nNo previous checkpoint found. Starting first ingestion.")

    try:
        weather = get_weather(city)

        # Create data directory if it does not exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # Create timestamped file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = data_dir / f"weather_{timestamp}.json"

        # Save raw API response
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(weather, file, indent=4)

        print("\nWeather Details")
        print("----------------")
        print(f"City: {weather['name']}")
        print(f"Temperature: {weather['main']['temp']}°C")
        print(f"Humidity: {weather['main']['humidity']}%")
        print(
            f"Condition: "
            f"{weather['weather'][0]['description']}"
        )

        print(f"\nRaw response saved to: {file_path}")

        # Update checkpoint only after successful ingestion
        save_checkpoint(city, str(file_path))

        print("Checkpoint updated successfully.")

    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            print(
                f"City '{city}' was not found. "
                "Please check the spelling."
            )
        elif error.response.status_code == 401:
            print("Unauthorized API key. Check your .env file.")
        else:
            print(f"API request failed: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()