import psycopg2
from unittest.mock import MagicMock, patch

from utils.database_functions import create_database, create_tables, insert_database

@patch("utils.database_functions.psycopg2.connect")
def test_connect_to_db(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    create_database()

    mock_cur.execute.assert_called_once_with("CREATE DATABASE headhunter")

@patch("utils.database_functions.get_connection")
def test_create_tables(mock_connection):
    mock_conn = MagicMock()
    mock_cur = MagicMock()

    mock_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    create_tables()

    assert mock_cur.execute.call_count == 2

@patch("utils.database_functions.get_objects_with_employers")
@patch("utils.database_functions.HeadHunterApi")
@patch("utils.database_functions.get_connection")
def test_insert_database(
    mock_get_connection,
    mock_hh_api,
    mock_get_objects
):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    hh_instance = mock_hh_api.return_value
    hh_instance.get_employers.return_value = [
        [{"id": 1, "name": "Test Company"}]
    ]
    vacancy = MagicMock()
    vacancy.employer_id = 1
    vacancy.title = "Python Dev"
    vacancy.salary_from = 100000
    vacancy.salary_to = 150000
    vacancy.salary = 150000
    vacancy.link = "http://test"

    mock_get_objects.return_value = [[vacancy]]

    insert_database()

    assert mock_cursor.executemany.call_count == 2




