import json
from pathlib import Path

import pandas as pd


def get_latest_json_file() -> Path:
    """Return the most recently created weather JSON file."""
    data_dir = Path("data")
    json_files = list(data_dir.glob("weather_*.json"))

    if not json_files:
        raise FileNotFoundError("No weather JSON files found in data/")

    return max(json_files, key=lambda file: file.stat().st_mtime)


def flatten_weather_json(json_file: Path) -> pd.DataFrame:
    """Read nested weather JSON and convert it into a flat DataFrame."""
    with open(json_file, "r", encoding="utf-8") as file:
        weather_data = json.load(file)

    # Flatten the main nested object
    main_data = pd.json_normalize(weather_data)

    # Extract the first weather condition from the weather array
    weather_data = pd.json_normalize(weather_data, record_path="weather")

    # Add the first weather condition to the main DataFrame
    main_data["weather_description"] = weather_data.iloc[0]["description"]
    main_data["weather_main"] = weather_data.iloc[0]["main"]

    return main_data


def main():
    latest_file = get_latest_json_file()

    print(f"Reading file: {latest_file}")

    df = flatten_weather_json(latest_file)

    output_file = Path("data") / "weather_flattened.csv"
    df.to_csv(output_file, index=False)

    print("\nFlattened DataFrame")
    print("-------------------")
    print(df.to_string(index=False))

    print(f"\nCSV saved to: {output_file}")


if __name__ == "__main__":
    main()