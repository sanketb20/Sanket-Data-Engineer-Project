import pandas as pd
import psycopg
import time
import os

from dotenv import load_dotenv

from cleaning import load_all_files, clean_data
from validation import validate_data
from logger import get_logger
from db_connection import get_connection


# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def connect_with_retry(max_retries=3, base_delay=1):
    """
    Connect to PostgreSQL with retry logic
    using exponential backoff.
    """

    for attempt in range(1, max_retries + 1):

        try:
            print(
                f"PostgreSQL connection attempt "
                f"{attempt}/{max_retries}"
            )

            connection = get_connection()

            print("PostgreSQL connection successful")

            return connection

        except psycopg.OperationalError as error:

            print(
                f"PostgreSQL connection failed: {error}"
            )

            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise

            delay = base_delay * (2 ** (attempt - 1))

            print(
                f"Retrying in {delay} second(s)..."
            )

            time.sleep(delay)


def convert_value(value):
    """
    Convert Pandas values into values that PostgreSQL/Psycopg
    can understand.
    """

    # Pandas missing values -> PostgreSQL NULL
    if pd.isna(value):
        return None

    # Pandas Timestamp -> Python datetime
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    # NumPy values -> native Python values
    if hasattr(value, "item"):
        return value.item()

    return value


def batch_load():

    # Create logger
    logger = get_logger("batch_load")

    logger.info("ETL pipeline started")

    try:

        # --------------------------------------------------
        # 1. EXTRACT
        # --------------------------------------------------

        df = load_all_files()

        logger.info(f"Records extracted: {len(df)}")

        # --------------------------------------------------
        # 2. TRANSFORM
        # --------------------------------------------------

        df = clean_data(df)

        logger.info(f"Records after cleaning: {len(df)}")

        # --------------------------------------------------
        # 3. VALIDATE
        # --------------------------------------------------

        valid_df, invalid_df = validate_data(df)

        logger.info(f"Valid records: {len(valid_df)}")
        logger.warning(f"Invalid records: {len(invalid_df)}")

        # --------------------------------------------------
        # 4. PREPARE BATCH
        # --------------------------------------------------

        records = []

        for _, row in valid_df.iterrows():

            record = (
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

            records.append(record)

        logger.info(
            f"Records prepared for batch insert: {len(records)}"
        )

        # --------------------------------------------------
        # 5. CONNECT TO POSTGRESQL WITH RETRY
        # --------------------------------------------------

        logger.info("Connecting to PostgreSQL")

        with connect_with_retry() as connection:

            logger.info("PostgreSQL connection successful")

            with connection.cursor() as cursor:

                # Remove previous test/load data
                cursor.execute("TRUNCATE TABLE shipments;")

                logger.info("Shipments table cleared")

                # --------------------------------------------------
                # 6. BATCH INSERT
                # --------------------------------------------------

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

                cursor.executemany(
                    insert_query,
                    records
                )

            connection.commit()

        logger.info("Batch insert completed successfully")
        logger.info(f"Total records inserted: {len(records)}")
        logger.info("ETL pipeline completed successfully")

        print("\nETL pipeline completed successfully!")
        print(f"Total records inserted: {len(records)}")

    except Exception as error:

        logger.exception(
            f"ETL pipeline failed: {error}"
        )

        print(f"\nETL pipeline failed: {error}")

        raise


if __name__ == "__main__":
    batch_load()