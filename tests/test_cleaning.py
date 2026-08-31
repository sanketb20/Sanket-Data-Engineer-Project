import pandas as pd

from cleaning import clean_data


def create_test_data():
    return pd.DataFrame([
        {
            "shipment_id": " SHP1001 ",
            "customer_id": " CUST001 ",
            "shipment_date": "2026-08-20",
            "origin": " Bangalore ",
            "destination": " Mumbai ",
            "status": " Delivered ",
            "weight_kg": "12.5",
            "shipping_cost": "450",
            "carrier": " BlueDart ",
            "delivery_date": "23/08/2026",
            "priority": " High ",
            "warehouse_id": " WH-BLR-01 ",
            "service_type": " Express ",
        }
    ])


def test_whitespace_is_removed():
    df = create_test_data()

    result = clean_data(df)

    assert result.iloc[0]["shipment_id"] == "SHP1001"
    assert result.iloc[0]["customer_id"] == "CUST001"
    assert result.iloc[0]["origin"] == "Bangalore"
    assert result.iloc[0]["destination"] == "Mumbai"
    assert result.iloc[0]["status"] == "Delivered"
    assert result.iloc[0]["carrier"] == "BlueDart"


def test_iso_date_is_converted():
    df = create_test_data()

    result = clean_data(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipment_date"]
    )

    assert result.iloc[0]["shipment_date"] == pd.Timestamp(
        "2026-08-20"
    )


def test_slash_date_is_converted():
    df = create_test_data()

    result = clean_data(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["delivery_date"]
    )

    assert result.iloc[0]["delivery_date"] == pd.Timestamp(
        "2026-08-23"
    )


def test_numeric_columns_are_converted():
    df = create_test_data()

    result = clean_data(df)

    assert pd.api.types.is_numeric_dtype(
        result["weight_kg"]
    )

    assert pd.api.types.is_numeric_dtype(
        result["shipping_cost"]
    )

    assert result.iloc[0]["weight_kg"] == 12.5
    assert result.iloc[0]["shipping_cost"] == 450


def test_empty_strings_become_missing():
    df = create_test_data()

    df.loc[0, "carrier"] = ""

    result = clean_data(df)

    assert pd.isna(result.iloc[0]["carrier"])


def test_invalid_numeric_values_become_missing():
    df = create_test_data()

    df.loc[0, "weight_kg"] = "invalid"
    df.loc[0, "shipping_cost"] = "invalid"

    result = clean_data(df)

    assert pd.isna(result.iloc[0]["weight_kg"])
    assert pd.isna(result.iloc[0]["shipping_cost"])


def test_duplicate_records_are_removed():
    df = create_test_data()

    df = pd.concat(
        [df, df],
        ignore_index=True
    )

    assert len(df) == 2

    result = clean_data(df)

    assert len(result) == 1