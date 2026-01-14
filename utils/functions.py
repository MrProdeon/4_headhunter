from __future__ import annotations

from src.Vacancy import Vacancy
from src.connector import HeadHunterApi
from src.FileWorker import JsonWorker

hh_api = HeadHunterApi({"User-Agent": "test for skypro"})
json_worker = JsonWorker("data/json_data.json")


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
    user_input = input("Хотите продолжить работу в этом сервисе? 1 - да, 2 - нет : ")
    while user_input not in ("1", "2"):
        user_input = input("Хотите продолжить работу в этом сервисе? 1 - да, 2 - нет")

    if user_input == "1":
        return True
    return False


def get_objects_with_employers(connector_object: HeadHunterApi):
    """Функция для получения всех вакансий определенного работодателя, используя его айди.
    Вернет список списков, в котором каждый список - это вакансии определенного работодателя.
    """
    vacancies = []
    for i in connector_object.get_ids(connector_object.get_employers()):
        keys = i.keys()
        vacancies.append(connector_object.get_vacancies(employer_id=list(keys)[0]))
    employer_list = []
    for i in vacancies:
        all_vacancies = Vacancy.cast_to_object_list(i)
        employer_list.append(all_vacancies)
    resulted_employer_list = []
    for j in employer_list:
        result = []
        for o in j:
            result.append(o)
        resulted_employer_list.append(result)
    return resulted_employer_list


def only_vacancies() -> None:
    while True:
        try:
            target = sorted(
                list(
                    map(
                        int,
                        input(
                            """По каким критериям отфильтровать вакансии?
1 - ключевые слова
2 - по диапазону зарплат
3 - по самым высоким зарплатам
4 - удалёнка или офис
5 - просмотреть уже записанные вакансии из файла (если этот пункт будет выбран, то будет обработан только он)
(Напишите в одну строку через пробел)
"""
                        )
                        .strip()
                        .split(),
                    )
                )
            )
        except ValueError:
            continue
        if all(number in (1, 2, 3, 4, 5) for number in target):

            if 5 in target:
                vacancies = json_worker.get_data()
                if len(vacancies) == 0:
                    print("Пусто")
                    if end_or_continue():
                        continue
                    break
                else:
                    vacancies_objects = dicts_to_objects(vacancies)
                    print_vacancies(vacancies_objects)
                    if end_or_continue():
                        continue
                    break

            if 1 in target:
                name = input("Введите ключевые слова: ")
                vacancies = hh_api.get_vacancies(name)
            else:
                vacancies = hh_api.get_vacancies()

            if 4 in target:
                work_f = input("1 - для поиска удалёнки, 2 - для поиска офиса, 3 - гибрид")
                while work_f not in ("1", "2", "3"):
                    work_f = input("1 - для поиска удалёнки, 2 - для поиска офиса, 3 - гибрид")
                if work_f == "1":
                    vacancies = [
                        vacancy
                        for vacancy in vacancies
                        if any(work_format["id"] == "REMOTE" for work_format in vacancy["work_format"])
                    ]
                if work_f == "2":
                    vacancies = [
                        vacancy
                        for vacancy in vacancies
                        if any(work_format["id"] == "ON_SITE" for work_format in vacancy["work_format"])
                    ]
                if work_f == "3":
                    vacancies = [
                        vacancy
                        for vacancy in vacancies
                        if any(work_format["id"] == "HYBRID" for work_format in vacancy["work_format"])
                    ]

            vacancies = Vacancy.cast_to_object_list(vacancies)

            if 2 in target:
                while True:
                    range_from_str = input("Введите начальную зарплату: ")
                    range_to_str = input("Введите конечную зарплату: ")
                    try:
                        range_from = int(range_from_str)
                        range_to = int(range_to_str)
                        break
                    except ValueError:
                        print("Введите число!")
                        continue

                vacancies = ranged_vacancies(vacancies, range_from, range_to)

            if 3 in target:
                n_str = input("Какое отобразить количество вакансий с максимальной ЗП?  ")
                while True:
                    try:
                        n = int(n_str)
                        break
                    except ValueError:
                        print("Введите число!")
                        continue
                vacancies = top_n(vacancies, n)

            to_file = input("Хотите записать вакансии в файл? 1 - да, 2 - нет : ")
            while to_file not in ("1", "2"):
                to_file = input("Хотите записать вакансии в файл? 1 - да, 2 - нет : ")
            if to_file == "1":
                for vacancy in vacancies:
                    json_worker.add_data(vacancy)

            print_vacancies(vacancies)

            if end_or_continue():
                continue
            break
