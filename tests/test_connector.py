# mypy: ignore-errors

from unittest.mock import patch

import requests

from src.connector import HeadHunterApi

params = {"text": "", "page": 0, "per_page": 100}


@patch("requests.get")
def test_headhunter_api(mock_get):
    mock_get.return_value.json.return_value = {"items": [{"id": 1, "name": "python-developer", "salary": 90000}]}

    hh_api = HeadHunterApi({"User-Agent": "test for skypro"})

    assert hh_api._connect(params, url="https://api.hh.ru/vacancies") == {
        "items": [{"id": 1, "name": "python-developer", "salary": 90000}]
    }
    assert hh_api.get_vacancies() == [{"id": 1, "name": "python-developer", "salary": 90000}]


@patch("requests.get")
def test_headhunter_api_error(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
    hh_api = HeadHunterApi({"User-Agent": "test for skypro"})
    try_connect = hh_api._connect(params, url="https://api.hh.ru/vacancies")

    assert try_connect is None

    hh_api.get_vacancies()

@patch("requests.get")
def test_get_employers(mock_get):
    mock_get.return_value.json.return_value = {"items" : ["test"]}
    mock_get.status_code = 200

    hh = HeadHunterApi({"User-Agent": "test for skypro"})

    assert hh.get_employers(["test", "test2"]) == [["test"], ["test"]]

def test_get_ids():
    hh = HeadHunterApi({"User-Agent": "test for skypro"})
    result = hh.get_ids([[{"id" : 1, "name" : "test1"}], [{"id" : 2, "name" : "test2"}]])
    assert result == [{1: 'test1'}, {2: 'test2'}]
