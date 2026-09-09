import json
from pathlib import Path
from datetime import datetime, timezone


STATE_FILE = Path("state/weather_checkpoint.json")


def load_checkpoint() -> dict:
    """Load the previous ingestion checkpoint."""
    if not STATE_FILE.exists():
        return {
            "completed_cities": [],
            "failed_cities": [],
            "last_successful_city": None,
            "last_successful_file": None,
            "last_successful_fetch_utc": None,
        }

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_checkpoint(
    city: str,
    source_file: str,
    status: str = "success",
    error: str = None,
) -> None:
    """Update the checkpoint after processing a city."""

    checkpoint = load_checkpoint()

    completed_cities = checkpoint.get("completed_cities", [])
    failed_cities = checkpoint.get("failed_cities", [])

    if status == "success":
        if city not in completed_cities:
            completed_cities.append(city)

        # Remove the city from failed list if it succeeds later
        failed_cities = [
            item for item in failed_cities
            if item.get("city") != city
        ]

        checkpoint.update({
            "completed_cities": completed_cities,
            "failed_cities": failed_cities,
            "last_successful_city": city,
            "last_successful_file": source_file,
            "last_successful_fetch_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        })

    elif status == "failed":
        failed_cities = [
            item for item in failed_cities
            if item.get("city") != city
        ]

        failed_cities.append({
            "city": city,
            "error": error,
            "failed_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        })

        checkpoint["failed_cities"] = failed_cities

    STATE_FILE.parent.mkdir(exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(checkpoint, file, indent=4)