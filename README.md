# A4 – Python ETL Pipeline

A production-style Python ETL pipeline that extracts shipment data from CSV and JSON files, normalizes the schema, cleans and validates the data, rejects invalid records, and loads valid records into PostgreSQL.

The project also includes retry-based database connectivity, structured logging, batch insertion, and automated unit testing using pytest.

---

## Project Overview

This ETL pipeline processes shipment data from multiple source files.

### ETL Flow

Source CSV / JSON Files
        ↓
Data Ingestion
        ↓
Schema Normalization
        ↓
Data Cleaning
        ↓
Data Validation
        ↓
Valid Records ──────────→ PostgreSQL
        │
        ↓
Invalid Records
        ↓
Rejected CSV

---

## Key Features

- Read shipment data from CSV and JSON files
- Normalize different source schemas into a standard shipment schema
- Remove leading and trailing whitespace
- Convert empty strings to missing values
- Convert shipment and delivery dates into datetime format
- Convert numeric fields into appropriate numeric types
- Remove duplicate records
- Validate mandatory shipment fields
- Validate shipment weight and shipping cost
- Separate valid and invalid records
- Store rejected records with rejection reasons
- Connect to PostgreSQL using Psycopg
- Use environment variables for database configuration
- Implement PostgreSQL connection retry logic with exponential backoff
- Perform batch insertion using `executemany`
- Truncate previous test/load data before batch loading
- Implement rotating file logging
- Maintain automated unit tests using pytest
- Achieve 83% overall test coverage

---

## Technologies Used

- Python 3.11
- Pandas
- PostgreSQL
- Psycopg
- pytest
- pytest-cov
- python-dotenv
- Git

---

## Project Structure

```text
A4-Python-ETL-Pipeline/
│
├── config/
│   └── schema.sql
│
├── rejected/
│   └── rejected_shipments.csv
│
├── source/
│   ├── shipments_day1.csv
│   ├── shipments_day2.csv
│   ├── shipments_day3.json
│   └── shipments_day4.json
│
├── src/
│   ├── batch_load.py
│   ├── check_dates.py
│   ├── cleaning.py
│   ├── create_table.py
│   ├── db_connection.py
│   ├── ingestion.py
│   ├── insert_one.py
│   ├── inspect_files.py
│   ├── logger.py
│   ├── read_files.py
│   ├── test_logger.py
│   └── validation.py
│
├── tests/
│   ├── test_batch_load.py
│   ├── test_check_dates.py
│   ├── test_cleaning.py
│   ├── test_create_table.py
│   ├── test_db_connection.py
│   ├── test_ingestion.py
│   ├── test_insert_one.py
│   ├── test_inspect_files.py
│   ├── test_read_files.py
│   └── test_validation.py
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md