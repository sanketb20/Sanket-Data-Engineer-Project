from unittest.mock import MagicMock, patch

import db_connection


def test_get_connection():
    mock_connection = MagicMock()

    with patch(
        "db_connection.psycopg.connect",
        return_value=mock_connection
    ) as mock_connect:

        result = db_connection.get_connection()

        assert result is mock_connection

        mock_connect.assert_called_once_with(
            host=db_connection.DB_HOST,
            port=db_connection.DB_PORT,
            dbname=db_connection.DB_NAME,
            user=db_connection.DB_USER,
            password=db_connection.DB_PASSWORD,
            connect_timeout=5,
        )


def test_test_connection():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)

    with patch(
        "db_connection.get_connection",
        return_value=mock_connection
    ):

        db_connection.test_connection()

    mock_cursor.execute.assert_called_once_with("SELECT 1;")
    mock_cursor.fetchone.assert_called_once()
    mock_connection.close.assert_called_once()