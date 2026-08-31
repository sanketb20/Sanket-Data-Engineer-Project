from pathlib import Path
import pandas as pd


SOURCE_FOLDER = Path("source")

STANDARD_COLUMNS = [
    "shipment_id",
    "customer_id",
    "shipment_date",
    "origin",
    "destination",
    "status",
    "weight_kg",
    "shipping_cost",
    "carrier",
    "delivery_date",
    "priority",
    "warehouse_id",
    "service_type",
]


def read_file(file):
    """Read a CSV or JSON file into a DataFrame."""

    if file.suffix.lower() == ".csv":
        return pd.read_csv(file)

    if file.suffix.lower() == ".json":
        return pd.read_json(file)

    return None


def normalize_schema(df):
    """Make the DataFrame match the standard shipment schema."""

    for column in STANDARD_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    df = df[STANDARD_COLUMNS]

    return df


dataframes = []

for file in SOURCE_FOLDER.iterdir():

    if not file.is_file():
        continue

    df = read_file(file)

    if df is None:
        continue

    df = normalize_schema(df)

    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

print("\nCombined DataFrame")
print("------------------")
print(combined_df)

print("\nShape:")
print(combined_df.shape)

print("\nColumns:")
print(list(combined_df.columns))