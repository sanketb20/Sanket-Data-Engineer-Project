import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

from insert_one import convert_value, insert_one_record


def test_convert_missing_value():
    result = convert_value(pd.NA)

    assert result is None


def test_convert_timestamp():
    timestamp = pd.Timestamp("2026-08-30")

    result = convert_value(timestamp)

    assert result == timestamp.to_pydatetime()


def test_convert_numpy_value():
    value = np.int64(100)

    result = convert_value(value)

    assert result == 100
    assert isinstance(result, int)


def test_convert_normal_value():
    value = "SHP9999"

    result = convert_value(value)

    assert result == value


def test_insert_one_record():

    valid_df = pd.DataFrame([
        {
            "shipment_id": "SHP9999",
            "customer_id": "CUST999",
            "shipment_date": pd.Timestamp("2026-08-30"),
            "origin": "Bangalore",
            "destination": "Mumbai",
            "status": "Delivered",
            "weight_kg": 10.5,
            "shipping_cost": 450.0,
            "carrier": "BlueDart",
            "delivery_date": pd.Timestamp("2026-09-01"),
            "priority": "Normal",
            "warehouse_id": "WH-BLR-01",
            "service_type": "Standard",
        }
    ])

    invalid_df = pd.DataFrame()

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with patch(
        "insert_one.load_all_files",
        return_value=valid_df
    ), patch(
        "insert_one.clean_data",
        return_value=valid_df
    ), patch(
        "insert_one.validate_data",
        return_value=(valid_df, invalid_df)
    ), patch(
        "insert_one.psycopg.connect",
        return_value=mock_connection
    ):

        insert_one_record()

    mock_cursor.execute.assert_called_once()

    mock_connection.commit.assert_called_once()

    mock_connection.close.assert_not_called()