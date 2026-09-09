from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/weather_all_cities.csv")


REQUIRED_COLUMNS = [
    "city",
    "country",
    "temperature_c",
    "humidity_percent",
    "weather_condition",
]


def validate_weather_data():
    """Validate the consolidated weather CSV file."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    dataframe = pd.read_csv(INPUT_FILE)

    errors = []

    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )

    # Check empty mandatory fields
    for column in REQUIRED_COLUMNS:
        if column in dataframe.columns:
            missing_count = dataframe[column].isna().sum()

            if missing_count > 0:
                errors.append(
                    f"{column} contains {missing_count} missing values"
                )

    # Check duplicate cities
    if "city" in dataframe.columns:
        duplicate_count = dataframe.duplicated(
            subset=["city", "country"]
        ).sum()

        if duplicate_count > 0:
            errors.append(
                f"Duplicate city records: {duplicate_count}"
            )

    # Check temperature range
    if "temperature_c" in dataframe.columns:
        invalid_temperature_count = (
            (dataframe["temperature_c"] < -90)
            | (dataframe["temperature_c"] > 60)
        ).sum()

        if invalid_temperature_count > 0:
            errors.append(
                f"Invalid temperature records: "
                f"{invalid_temperature_count}"
            )

    # Check humidity range
    if "humidity_percent" in dataframe.columns:
        invalid_humidity_count = (
            (dataframe["humidity_percent"] < 0)
            | (dataframe["humidity_percent"] > 100)
        ).sum()

        if invalid_humidity_count > 0:
            errors.append(
                f"Invalid humidity records: "
                f"{invalid_humidity_count}"
            )

    print("\n========== DATA QUALITY REPORT ==========")
    print(f"Input file: {INPUT_FILE}")
    print(f"Total records: {len(dataframe)}")
    print(f"Total columns: {len(dataframe.columns)}")

    if errors:
        print("\nValidation status: FAILED")

        for error in errors:
            print(f"- {error}")

        return False

    print("Validation status: PASSED")
    print("No data-quality issues found.")
    print("=========================================")

    return True


if __name__ == "__main__":
    validate_weather_data()