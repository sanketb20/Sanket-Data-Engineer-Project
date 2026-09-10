import json
import time
from pathlib import Path
from datetime import datetime

from api_client import get_weather
from checkpoint import load_checkpoint, save_checkpoint


CITIES_FILE = Path("config/cities.txt")
DATA_DIR = Path("data")

# Delay between API requests to avoid excessive API calls
REQUEST_DELAY_SECONDS = 2


def load_cities():
    """Read city names from the configuration file."""

    if not CITIES_FILE.exists():
        raise FileNotFoundError(
            f"Cities configuration file not found: {CITIES_FILE}"
        )

    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def ingest_multiple_cities():
    """Fetch weather data for multiple cities and resume from checkpoint."""

    cities = load_cities()
    checkpoint = load_checkpoint()

    completed_cities = set(
        checkpoint.get("completed_cities", [])
    )

    print(f"Total cities configured: {len(cities)}")
    print(f"Already completed: {len(completed_cities)}")

    successful = 0
    failed = 0
    skipped = 0

    for index, city in enumerate(cities, start=1):

        # Skip cities that were already processed successfully
        if city in completed_cities:
            print(f"\n[{index}/{len(cities)}] Skipping: {city}")
            print("Already completed in checkpoint.")

            skipped += 1
            continue

        print(f"\n[{index}/{len(cities)}] Processing: {city}")

        try:
            # Call the weather API
            weather = get_weather(city)

            # Create data directory if it does not exist
            DATA_DIR.mkdir(exist_ok=True)

            # Generate timestamp for the output file
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            # Convert city name into a safe filename
            safe_city_name = city.lower().replace(" ", "_")

            file_path = (
                DATA_DIR
                / f"weather_{safe_city_name}_{timestamp}.json"
            )

            # Save raw API response
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(weather, file, indent=4)

            # Update checkpoint after successful ingestion
            save_checkpoint(
                city=city,
                source_file=str(file_path),
                status="success",
            )

            print(f"Successfully saved: {file_path}")

            successful += 1

        except Exception as error:

            print(f"Failed to process {city}: {error}")

            # Record failed city in checkpoint
            save_checkpoint(
                city=city,
                source_file="",
                status="failed",
                error=str(error),
            )

            failed += 1

        # Rate limiting between API requests
        if index < len(cities):
            print(
                f"Waiting {REQUEST_DELAY_SECONDS} seconds "
                "before the next request..."
            )

            time.sleep(REQUEST_DELAY_SECONDS)

    print("\n========== INGESTION SUMMARY ==========")
    print(f"Successful cities: {successful}")
    print(f"Skipped cities: {skipped}")
    print(f"Failed cities: {failed}")
    print("=======================================")


if __name__ == "__main__":
    ingest_multiple_cities()