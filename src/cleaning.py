import pandas as pd

from ingestion import SOURCE_FOLDER, STANDARD_COLUMNS, read_file, normalize_schema


def load_all_files():
    """Read, normalize, and combine all source files."""

    dataframes = []

    for file in SOURCE_FOLDER.iterdir():

        if not file.is_file():
            continue

        df = read_file(file)

        if df is None:
            continue

        df = normalize_schema(df)

        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def clean_data(df):
    """Clean shipment data."""

    # 1. Remove leading/trailing whitespace from text columns
    text_columns = [
        "shipment_id",
        "customer_id",
        "origin",
        "destination",
        "status",
        "carrier",
        "priority",
        "warehouse_id",
        "service_type",
    ]

    for column in text_columns:
        df[column] = df[column].str.strip()

    # 2. Convert empty strings to missing values
    df = df.replace("", pd.NA)

    # 3. Convert date columns to datetime
    # Handle both YYYY-MM-DD and DD/MM/YYYY formats safely.

    for column in ["shipment_date", "delivery_date"]:

        # Convert the column to object first so datetime values
        # can be assigned safely.
        df[column] = df[column].astype("object")

        values = df[column].astype("string").str.strip()

        # ISO format: YYYY-MM-DD
        iso_mask = values.str.match(
            r"^\d{4}-\d{2}-\d{2}$",
            na=False
        )

        df.loc[iso_mask, column] = pd.to_datetime(
            values[iso_mask],
            errors="coerce",
            format="%Y-%m-%d"
        )

        # Slash format: DD/MM/YYYY
        slash_mask = values.str.match(
            r"^\d{2}/\d{2}/\d{4}$",
            na=False
        )

        df.loc[slash_mask, column] = pd.to_datetime(
            values[slash_mask],
            errors="coerce",
            format="%d/%m/%Y"
        )

        # Convert the complete column to datetime
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    # 4. Convert numeric columns
    df["weight_kg"] = pd.to_numeric(
        df["weight_kg"],
        errors="coerce",
    )

    df["shipping_cost"] = pd.to_numeric(
        df["shipping_cost"],
        errors="coerce",
    )

    # 5. Remove exact duplicate records
    df = df.drop_duplicates()

    return df


if __name__ == "__main__":

    df = load_all_files()

    print("Before cleaning:")
    print(df.shape)

    df = clean_data(df)

    print("\nAfter cleaning:")
    print(df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nSample data:")
    print(df.head())