from __future__ import annotations

from src.Vacancy import Vacancy


def top_n(vacancies: list[Vacancy], n: int) -> list:
    """Функция для отображения топовых вакансий по зарплате.
    Количество отображения регулируется параметром n"""

    # top_vacancies = sorted(vacancies, key=lambda x: x.salary_from)
    #
    # top_n_vacancies = [top_vacancies[i] for i in range(n)]

    length = len(vacancies)
    for i in range(length):
        for j in range(0, length - i - 1):
            if vacancies[j] < vacancies[j + 1]:
                vacancies[j], vacancies[j + 1] = vacancies[j + 1], vacancies[j]

    return vacancies[:n]


def ranged_vacancies(vacancies: list[Vacancy], range_from: int | float, range_to: int | float | None = None) -> list:
    """Функция для отображения вакансий в выбранном диапазоне зарплат."""

    if range_to is None:
        ranged_vacancies = [vacancy for vacancy in vacancies if vacancy >= range_from]
    else:
        ranged_vacancies = [vacancy for vacancy in vacancies if range_from <= vacancy <= range_to]

    return ranged_vacancies


def print_vacancies(vacancies: list[Vacancy]) -> str:
    """Функция для фомирования строки и вывода этой строки"""

    resulted_string = ""

    for vacancy in vacancies:
        string = f"{vacancy.title} От: {vacancy.salary_from}, до : {vacancy.salary_to}, {vacancy.link}\n"
        resulted_string += string

    print(resulted_string)
    return resulted_string


def dicts_to_objects(vacancies: list[dict]) -> list:
    """Функция для преобразования списка словарей из читаемого файла в список объектов класса Vacancy"""
    vacancy_list = []
    for vacancy in vacancies:
        vacancy_list.append(Vacancy(**vacancy))

    return vacancy_list


def end_or_continue() -> bool:
    """Вспомогательная функция для продолжения или остановки программы"""
    user_input = input("Хотите продолжить работу с программой? 1 - да, 2 - нет : ")
    while user_input not in ("1", "2"):
        user_input = input("Хотите продолжить работу с программой? 1 - да, 2 - нет")

    if user_input == "1":
        return True
    return False
