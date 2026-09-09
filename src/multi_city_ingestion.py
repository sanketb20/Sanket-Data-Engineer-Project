import json
import time
from pathlib import Path
from datetime import datetime

from api_client import get_weather
from checkpoint import load_checkpoint, save_checkpoint


CITIES_FILE = Path("config/cities.txt")
DATA_DIR = Path("data")

REQUEST_DELAY = 2


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
    """Fetch weather data and resume from the checkpoint."""

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

        # Skip cities already processed successfully
        if city in completed_cities:
            print(f"\n[{index}/{len(cities)}] Skipping: {city}")
            print("Already completed in checkpoint.")
            skipped += 1
            continue

        print(f"\n[{index}/{len(cities)}] Processing: {city}")

        try:
            weather = get_weather(city)

            DATA_DIR.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_city_name = city.lower().replace(" ", "_")

            file_path = (
                DATA_DIR
                / f"weather_{safe_city_name}_{timestamp}.json"
            )

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(weather, file, indent=4)

            save_checkpoint(
                city=city,
                source_file=str(file_path),
                status="success",
            )

            print(f"Successfully saved: {file_path}")

            successful += 1

        except Exception as error:

            print(f"Failed to process {city}: {error}")

            save_checkpoint(
                city=city,
                source_file="",
                status="failed",
                error=str(error),
            )

            failed += 1

        if index < len(cities):
            print(f"Waiting {REQUEST_DELAY} seconds...")
            time.sleep(REQUEST_DELAY)

    print("\n========== INGESTION SUMMARY ==========")
    print(f"Successful cities: {successful}")
    print(f"Skipped cities: {skipped}")
    print(f"Failed cities: {failed}")
    print("=======================================")


if __name__ == "__main__":
    ingest_multiple_cities()