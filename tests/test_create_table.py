from unittest.mock import MagicMock, patch

import create_table


def test_create_table():

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    schema_sql = """
    CREATE TABLE test_table (
        id INTEGER
    );
    """

    with patch(
        "create_table.Path.read_text",
        return_value=schema_sql
    ) as mock_read_text:

        with patch(
            "create_table.psycopg.connect",
            return_value=mock_connection
        ) as mock_connect:

            create_table.create_table()

    mock_read_text.assert_called_once_with(encoding="utf-8")

    mock_connect.assert_called_once()

    mock_cursor.execute.assert_called_once_with(schema_sql)

    mock_connection.commit.assert_called_once()