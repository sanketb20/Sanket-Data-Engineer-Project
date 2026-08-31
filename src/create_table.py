import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def create_table():
    schema_file = Path("config/schema.sql")
    schema_sql = schema_file.read_text(encoding="utf-8")

    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute(schema_sql)

        connection.commit()

    print("Shipments table created successfully!")


if __name__ == "__main__":
    create_table()