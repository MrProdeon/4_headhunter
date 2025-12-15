from unittest.mock import mock_open, patch
from src.FileWorker import JsonWorker
from src.Vacancy import Vacancy

vacancy = Vacancy("developer", "https", 90000, 100000)

def test_json_worker():
    data = JsonWorker("add_test.json")
    m = mock_open(read_data='{"id" : 1, "name" : "python-developer", "salary" : 90000}')
    with patch("builtins.open", m):
        result = data.get_data("test.json")

    assert result == {"id" : 1, "name" : "python-developer", "salary" : 90000}

    m2 = mock_open(read_data = "")
    with patch("builtins.open", m2):
        result2 = data.get_data("test.json")

    assert result2 == []

def test_json_worker_nofile():
    data = JsonWorker("error")

    assert data.get_data("error") == []


def test_add_data():
    m = mock_open(read_data='[{"title" : 1, "link" : "python-developer", "salary" : 90000, "description" : "no"}]')
    data = JsonWorker("add_test.json")

    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        data.add_data(vacancy)

    mock_dump.assert_called_once()

