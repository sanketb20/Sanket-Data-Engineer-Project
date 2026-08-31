import pandas as pd

from ingestion import read_file, normalize_schema


def test_read_csv_file(tmp_path):
    file = tmp_path / "test.csv"

    file.write_text(
        "shipment_id,customer_id\n"
        "SHP9999,CUST999\n"
    )

    result = read_file(file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["shipment_id"] == "SHP9999"


def test_read_json_file(tmp_path):
    file = tmp_path / "test.json"

    file.write_text(
        '[{"shipment_id": "SHP9999", "customer_id": "CUST999"}]'
    )

    result = read_file(file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["shipment_id"] == "SHP9999"


def test_read_unsupported_file_returns_none(tmp_path):
    file = tmp_path / "test.txt"

    file.write_text("unsupported file")

    result = read_file(file)

    assert result is None


def test_normalize_schema_adds_missing_columns():
    df = pd.DataFrame({
        "shipment_id": ["SHP9999"],
        "customer_id": ["CUST999"],
    })

    result = normalize_schema(df)

    assert list(result.columns) == [
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

    assert pd.isna(result.iloc[0]["shipment_date"])
    assert pd.isna(result.iloc[0]["status"])


def test_normalize_schema_preserves_existing_data():
    df = pd.DataFrame({
        "shipment_id": ["SHP9999"],
        "customer_id": ["CUST999"],
        "status": ["Delivered"],
    })

    result = normalize_schema(df)

    assert result.iloc[0]["shipment_id"] == "SHP9999"
    assert result.iloc[0]["customer_id"] == "CUST999"
    assert result.iloc[0]["status"] == "Delivered"