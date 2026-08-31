import os
import pandas as pd
import psycopg

from dotenv import load_dotenv

from cleaning import load_all_files, clean_data
from validation import validate_data


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def convert_value(value):
    """
    Convert Pandas/NumPy values into values that psycopg can
    send to PostgreSQL.
    """

    # Pandas missing values -> PostgreSQL NULL
    if pd.isna(value):
        return None

    # Pandas Timestamp -> Python datetime
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    # NumPy numeric values -> native Python values
    if hasattr(value, "item"):
        return value.item()

    return value


def insert_one_record():

    # 1. Extract
    df = load_all_files()

    # 2. Clean
    df = clean_data(df)

    # 3. Validate
    valid_df, invalid_df = validate_data(df)

    print(f"Valid records available: {len(valid_df)}")
    print(f"Invalid records available: {len(invalid_df)}")

    # 4. Select first valid record
    row = valid_df.iloc[0]

    print(f"Preparing shipment: {row['shipment_id']}")

    # 5. Convert Pandas values to database-compatible values
    values = (
        convert_value(row["shipment_id"]),
        convert_value(row["customer_id"]),
        convert_value(row["shipment_date"]),
        convert_value(row["origin"]),
        convert_value(row["destination"]),
        convert_value(row["status"]),
        convert_value(row["weight_kg"]),
        convert_value(row["shipping_cost"]),
        convert_value(row["carrier"]),
        convert_value(row["delivery_date"]),
        convert_value(row["priority"]),
        convert_value(row["warehouse_id"]),
        convert_value(row["service_type"]),
    )

    print("Values prepared for PostgreSQL.")

    # 6. Connect to PostgreSQL
    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as connection:

        # 7. Insert record
        with connection.cursor() as cursor:

            insert_query = """
                INSERT INTO shipments (
                    shipment_id,
                    customer_id,
                    shipment_date,
                    origin,
                    destination,
                    status,
                    weight_kg,
                    shipping_cost,
                    carrier,
                    delivery_date,
                    priority,
                    warehouse_id,
                    service_type
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                );
            """

            cursor.execute(
                insert_query,
                values
            )

        connection.commit()

    print(f"Inserted shipment successfully: {row['shipment_id']}")


if __name__ == "__main__":
    insert_one_record()