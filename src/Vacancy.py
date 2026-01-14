from __future__ import annotations


class Vacancy:
    """Класс для работы с вакансиями.
    У каждой вакансии должно быть указано название, ссылка на вакансию, зарплата и описание.
    Объекты этого метода поддерживают сравнение между собой. Сравнение происходит по зарплате.
    Прописаны приватные методы валидации, которые используются при инициализации объекта.
    Валидация проверяет указана ли ЗП и в числовом ли виде, если она не указана или указана строкой, то ставим 0.
    Так же проверяем указано ли название. Если нет, то прописываем Без названия.
    """

    __slots__ = ("title", "link", "salary_from", "salary_to", "description", "employer", "employer_id")

    def __init__(self, title: str, link: str, salary_from: int | float | None, salary_to: int | float | None, employer : str, employer_id : str):
        self.title = self.__validate_title(title)
        self.link = link
        self.salary_from = self.__validate_salary(salary_from)
        self.salary_to = self.__validate_salary(salary_to)
        self.employer = employer
        self.employer_id = employer_id

    def __gt__(self, other : Vacancy | int | float) -> bool:
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        elif isinstance(other, int) or isinstance(other, float):
            return self.salary > other
        raise ValueError("Переданы несравнимые данные")

    def __ge__(self, other : Vacancy | int | float) -> bool:
        if isinstance(other, Vacancy):
            return self.salary >= other.salary
        elif isinstance(other, int) or isinstance(other, float):
            return self.salary >= other
        raise ValueError("Переданы несравнимые данные")

    def __lt__(self, other : Vacancy | int | float) -> bool:
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        elif isinstance(other, int) or isinstance(other, float):
            return self.salary < other
        raise ValueError("Переданы несравнимые данные")

    def __le__(self, other : Vacancy | int | float) -> bool:
        if isinstance(other, Vacancy):
            return self.salary <= other.salary
        elif isinstance(other, int) or isinstance(other, float):
            return self.salary <= other
        raise ValueError("Переданы несравнимые данные")

    @property
    def salary(self)  -> int | float:
        return max(self.salary_from, self.salary_to)

    @staticmethod
    def __validate_title(title: str) -> str:
        """Метод для валидации названия. Если не передали ничего или не строку, то будет без названия"""
        if not isinstance(title, str) or not title:
            title = "Без названия"
        else:
            title = title
        return title

    @staticmethod
    def __validate_salary(salary: int | float | None) -> int:
        """Метод для валидации зарплаты. Если зарплата не число, то вернет 0"""

        if isinstance(salary, (int, float)):
            return int(salary)

        if salary is None or isinstance(salary, str):
            return 0

        return 0

    @staticmethod
    def cast_to_object_list(vacancies: list[dict]) -> list:
        """Методя для преобразования списка словарей в список объектов класса Vacancy"""
        vacancy_list = []
        for vacancy in vacancies:

            employer = vacancy.get("employer")
            if not employer or "id" not in employer:
                continue

            salary = vacancy.get("salary")
            salary_from = salary.get("from") if salary else None
            salary_to = salary.get("to") if salary else None

            vacancy_list.append(
                Vacancy(
                    vacancy.get("name", "No name"),
                    vacancy.get("alternate_url", ""),
                    salary_from,
                    salary_to,
                    vacancy.get("employer", {}).get("name", "No employer"),
                    vacancy.get("employer", {}).get("id", 0)
                )
            )

        return vacancy_list
