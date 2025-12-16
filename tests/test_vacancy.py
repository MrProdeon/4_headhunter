# mypy: ignore-errors

from src.Vacancy import Vacancy


def test_init():
    vacancy = Vacancy("developer", "https", 90000, 100000)
    assert vacancy.title == "developer"
    assert vacancy.link == "https"
    assert vacancy.salary_from == 90000
    assert vacancy.salary_to == 100000
    assert vacancy.salary == 100000


def test_validate():
    vacancy = Vacancy(None, "https", None, None)
    assert vacancy.title == "Без названия"
    assert vacancy.salary == 0


def test_cast_to_object_list():
    vacancies = [{"name": "developer", "alternate_url": "https", "salary": {"from": 90000, "to": 100000}}]

    result = Vacancy.cast_to_object_list(vacancies)

    assert len(result) == 1
    assert result[0].salary == 100000


def test_magic_methods():
    vacancy = Vacancy("developer", "https", 90000, 100000)
    assert vacancy > 50000
    assert vacancy >= 90000
    assert vacancy < 150000
    assert vacancy <= 100000
