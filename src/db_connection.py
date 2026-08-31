import os
import psycopg

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5,
    )

    return connection


def test_connection():
    """
    Test PostgreSQL database connectivity.
    """

    connection = get_connection()

    print("Connected to PostgreSQL successfully!")

    with connection.cursor() as cursor:

        cursor.execute("SELECT 1;")

        result = cursor.fetchone()

        print("Database test result:", result)

    connection.close()

    print("Connection closed.")


if __name__ == "__main__":
    test_connection()