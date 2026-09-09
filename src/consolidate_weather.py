import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "weather_all_cities.csv"


def read_weather_files():
    """Read all weather JSON files from the data directory."""

    records = []

    for file_path in DATA_DIR.glob("weather_*.json"):

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                weather = json.load(file)

            record = {
                "city": weather.get("name"),
                "country": weather.get("sys", {}).get("country"),
                "temperature_c": weather.get("main", {}).get("temp"),
                "feels_like_c": weather.get("main", {}).get("feels_like"),
                "minimum_temperature_c": weather.get("main", {}).get("temp_min"),
                "maximum_temperature_c": weather.get("main", {}).get("temp_max"),
                "pressure_hpa": weather.get("main", {}).get("pressure"),
                "humidity_percent": weather.get("main", {}).get("humidity"),
                "wind_speed_mps": weather.get("wind", {}).get("speed"),
                "weather_condition": (
                    weather.get("weather", [{}])[0].get("main")
                ),
                "weather_description": (
                    weather.get("weather", [{}])[0].get("description")
                ),
                "latitude": weather.get("coord", {}).get("lat"),
                "longitude": weather.get("coord", {}).get("lon"),
                "api_timestamp": weather.get("dt"),
                "source_file": file_path.name,
            }

            records.append(record)

        except json.JSONDecodeError:
            print(f"Invalid JSON file skipped: {file_path}")

        except Exception as error:
            print(f"Error reading {file_path}: {error}")

    return records


def consolidate_weather_data():
    """Combine all weather JSON files into one CSV file."""

    records = read_weather_files()

    if not records:
        print("No weather JSON files found.")
        return

    dataframe = pd.DataFrame(records)

    # Remove duplicate city records and retain the latest occurrence
    dataframe = dataframe.drop_duplicates(
        subset=["city", "country"],
        keep="last"
    )

    dataframe = dataframe.sort_values(
        by=["country", "city"]
    )

    dataframe.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print(f"Total records consolidated: {len(dataframe)}")
    print(f"CSV saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    consolidate_weather_data()