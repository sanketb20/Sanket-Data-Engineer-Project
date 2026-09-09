import json
from pathlib import Path

import pandas as pd
import pytest


def test_cities_file_exists():
    """Check that the city configuration file exists."""

    cities_file = Path("config/cities.txt")

    assert cities_file.exists()


def test_cities_file_contains_cities():
    """Check that the cities file contains valid city names."""

    cities_file = Path("config/cities.txt")

    with open(cities_file, "r", encoding="utf-8") as file:
        cities = [
            line.strip()
            for line in file
            if line.strip()
        ]

    assert len(cities) > 0
    assert "Bengaluru" in cities


def test_weather_json_files_exist():
    """Check that weather JSON files were created."""

    data_directory = Path("data")

    json_files = list(
        data_directory.glob("weather_*.json")
    )

    assert len(json_files) > 0


def test_weather_json_structure():
    """Check the structure of one weather JSON file."""

    data_directory = Path("data")

    json_files = list(
        data_directory.glob("weather_*.json")
    )

    assert len(json_files) > 0

    with open(json_files[0], "r", encoding="utf-8") as file:
        weather = json.load(file)

    assert "name" in weather
    assert "main" in weather
    assert "weather" in weather
    assert "sys" in weather


def test_consolidated_csv_exists():
    """Check that the consolidated CSV exists."""

    csv_file = Path("data/weather_all_cities.csv")

    assert csv_file.exists()


def test_consolidated_csv_has_records():
    """Check that the consolidated CSV contains records."""

    csv_file = Path("data/weather_all_cities.csv")

    dataframe = pd.read_csv(csv_file)

    assert len(dataframe) > 0


def test_required_columns_exist():
    """Check that required columns exist in the CSV."""

    csv_file = Path("data/weather_all_cities.csv")

    dataframe = pd.read_csv(csv_file)

    required_columns = [
        "city",
        "country",
        "temperature_c",
        "humidity_percent",
        "weather_condition",
    ]

    for column in required_columns:
        assert column in dataframe.columns


def test_no_duplicate_cities():
    """Check that city and country combinations are unique."""

    csv_file = Path("data/weather_all_cities.csv")

    dataframe = pd.read_csv(csv_file)

    duplicate_count = dataframe.duplicated(
        subset=["city", "country"]
    ).sum()

    assert duplicate_count == 0


def test_temperature_values_are_valid():
    """Check that temperature values are within a reasonable range."""

    csv_file = Path("data/weather_all_cities.csv")

    dataframe = pd.read_csv(csv_file)

    assert dataframe["temperature_c"].notna().all()
    assert dataframe["temperature_c"].between(-90, 60).all()


def test_humidity_values_are_valid():
    """Check that humidity values are between 0 and 100."""

    csv_file = Path("data/weather_all_cities.csv")

    dataframe = pd.read_csv(csv_file)

    assert dataframe["humidity_percent"].notna().all()
    assert dataframe["humidity_percent"].between(0, 100).all()