import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

import batch_load


def test_connect_with_retry_success():

    mock_connection = MagicMock()

    with patch(
        "batch_load.get_connection",
        return_value=mock_connection
    ) as mock_get_connection:

        result = batch_load.connect_with_retry()

    assert result is mock_connection
    mock_get_connection.assert_called_once()


def test_connect_with_retry_retries():

    mock_connection = MagicMock()

    with patch(
        "batch_load.get_connection",
        side_effect=[
            batch_load.psycopg.OperationalError("Connection failed"),
            batch_load.psycopg.OperationalError("Connection failed"),
            mock_connection,
        ]
    ) as mock_get_connection, patch(
        "batch_load.time.sleep"
    ) as mock_sleep:

        result = batch_load.connect_with_retry(
            max_retries=3,
            base_delay=1
        )

    assert result is mock_connection

    assert mock_get_connection.call_count == 3

    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)


def test_convert_value_missing():

    assert batch_load.convert_value(pd.NA) is None


def test_convert_value_timestamp():

    timestamp = pd.Timestamp("2026-08-30")

    result = batch_load.convert_value(timestamp)

    assert result == timestamp.to_pydatetime()


def test_convert_value_numpy():

    value = np.int64(100)

    result = batch_load.convert_value(value)

    assert result == 100
    assert isinstance(result, int)


def test_convert_value_normal():

    value = "SHP9999"

    assert batch_load.convert_value(value) == value


def test_batch_load_success():

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
        "batch_load.load_all_files",
        return_value=valid_df
    ), patch(
        "batch_load.clean_data",
        return_value=valid_df
    ), patch(
        "batch_load.validate_data",
        return_value=(valid_df, invalid_df)
    ), patch(
        "batch_load.connect_with_retry",
        return_value=mock_connection
    ):

        batch_load.batch_load()

    mock_cursor.execute.assert_called_once_with(
        "TRUNCATE TABLE shipments;"
    )

    mock_cursor.executemany.assert_called_once()

    mock_connection.commit.assert_called_once()


def test_batch_load_failure():

    with patch(
        "batch_load.load_all_files",
        side_effect=Exception("Test failure")
    ), patch(
        "batch_load.get_logger"
    ) as mock_logger:

        logger = mock_logger.return_value

        try:
            batch_load.batch_load()
        except Exception as error:
            assert str(error) == "Test failure"

        logger.exception.assert_called_once()
        
