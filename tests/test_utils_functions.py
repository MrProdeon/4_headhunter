import src.connector
from utils.functions import top_n, ranged_vacancies, print_vacancies, end_or_continue, get_objects_with_employers
from src.Vacancy import Vacancy
import pytest
from unittest.mock import patch

@pytest.mark.parametrize("_list, n, expected", [
    ([1, 2, 3], 2, [3, 2]),
    ([100, 500, 1000, 1500], 1, [1500]),
    ([123123, 656565, 989898], 3, [989898, 656565, 123123])
])
def test_top_n(_list, n, expected):
    assert top_n(_list,n) == expected


first = Vacancy("developer", "https", 90000, 100000, "test", "1")
second = Vacancy("product", "https", 105000, 150000, "test1", "2")
third = Vacancy("developer3", "https", 200000, 250000, "test3", "3")
@pytest.mark.parametrize("list_vacancies, range_from, range_to, expected", [
    ([first, second, third], 200000, None, [third]),
    ([first, second, third], 90000, 250000, [first, second, third]),
    ([first, second, third], 300000, 500000, [])
])
def test_ranged_vacancies(list_vacancies, range_from, range_to, expected):
    assert ranged_vacancies(list_vacancies, range_from, range_to) == expected

def test_print_vacancies(capsys):
    print_vacancies([first])
    rs = capsys.readouterr()
    assert rs.out == "developer От: 90000, до : 100000, https\n\n"

@patch("builtins.input")
def test_end_or_continue(mock_input):
    mock_input.return_value = "1"
    assert end_or_continue() == True

    mock_input.return_value = "2"
    assert end_or_continue() == False


obj = src.connector.HeadHunterApi({"User-Agent": "test for skypro"})
@patch("src.Vacancy.Vacancy.cast_to_object_list")
@patch("src.connector.HeadHunterApi.get_vacancies")
@patch("src.connector.HeadHunterApi.get_employers")
def test_get_objects_with_employers(mock_employers, mock_vacancies, mock_cast):
    mock_employers.return_value = [[{"id" : 1, "name" : "test1"}]]
    mock_vacancies.return_value = [{"employer" : {"name" : "test", "id" : 1},
                                    "salary" : {"from" : 100, "to" : 200},
                                    "alternate_url" : "https",
                                    "name" : "test1"}]
    mock_cast.return_value = ["sucess_test"]
    assert get_objects_with_employers(obj) == [["sucess_test"]]



