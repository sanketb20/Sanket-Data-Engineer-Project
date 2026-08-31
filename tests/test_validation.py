import pandas as pd

from validation import validate_data


def create_valid_data():
    return pd.DataFrame([
        {
            "shipment_id": "SHP1001",
            "customer_id": "CUST001",
            "shipment_date": pd.Timestamp("2026-08-20"),
            "origin": "Bangalore",
            "destination": "Mumbai",
            "status": "Delivered",
            "weight_kg": 12.5,
            "shipping_cost": 450.0,
        }
    ])


def test_valid_record():
    df = create_valid_data()

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 1
    assert len(invalid_df) == 0
    assert valid_df.iloc[0]["rejection_reason"] == ""


def test_missing_mandatory_field():
    df = create_valid_data()

    df.loc[0, "customer_id"] = None

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert "Missing customer_id" in invalid_df.iloc[0]["rejection_reason"]


def test_invalid_weight():
    df = create_valid_data()

    df.loc[0, "weight_kg"] = 0

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert "Invalid weight_kg" in invalid_df.iloc[0]["rejection_reason"]


def test_negative_weight():
    df = create_valid_data()

    df.loc[0, "weight_kg"] = -5

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert "Invalid weight_kg" in invalid_df.iloc[0]["rejection_reason"]


def test_negative_shipping_cost():
    df = create_valid_data()

    df.loc[0, "shipping_cost"] = -100

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1
    assert "Invalid shipping_cost" in invalid_df.iloc[0]["rejection_reason"]


def test_multiple_validation_errors():
    df = create_valid_data()

    df.loc[0, "customer_id"] = None
    df.loc[0, "weight_kg"] = -5
    df.loc[0, "shipping_cost"] = -100

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1

    reason = invalid_df.iloc[0]["rejection_reason"]

    assert "Missing customer_id" in reason
    assert "Invalid weight_kg" in reason
    assert "Invalid shipping_cost" in reason


def test_valid_and_invalid_records_are_separated():
    valid_record = {
        "shipment_id": "SHP1001",
        "customer_id": "CUST001",
        "shipment_date": pd.Timestamp("2026-08-20"),
        "origin": "Bangalore",
        "destination": "Mumbai",
        "status": "Delivered",
        "weight_kg": 12.5,
        "shipping_cost": 450.0,
    }

    invalid_record = {
        "shipment_id": "SHP1002",
        "customer_id": None,
        "shipment_date": pd.Timestamp("2026-08-20"),
        "origin": "Delhi",
        "destination": "Mumbai",
        "status": "Pending",
        "weight_kg": -2,
        "shipping_cost": -50,
    }

    df = pd.DataFrame([valid_record, invalid_record])

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 1
    assert len(invalid_df) == 1

    assert valid_df.iloc[0]["shipment_id"] == "SHP1001"
    assert invalid_df.iloc[0]["shipment_id"] == "SHP1002"