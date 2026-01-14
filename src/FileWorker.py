import json
from abc import ABC, abstractmethod

from src.Vacancy import Vacancy
from typing import Any


class FileWorker(ABC):

    @abstractmethod
    def get_data(self) -> list:
        pass

    @abstractmethod
    def add_data(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def delete_data(self) -> None:
        pass


class JsonWorker(FileWorker):

    def __init__(self, filename: str = "data/json_data.json") -> None:
        self.__filename = filename

    def get_data(self) -> Any:
        """Чтение JSON-файла и получение данных о вакансиях из него.
        Если файл пуст или не существует, вернет пустой список"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

                return data

        except FileNotFoundError:
            return []

    def add_data(self, vacancy: Vacancy) -> None:
        """Добавление вакансий в JSON-файл.
        Формируется словарь на основе атрибутов объекта и добавляется в список, а после
        этого список с новыми данными сохраняется в файл."""
        with open(self.__filename, "a+", encoding="utf-8") as file:
            file.seek(0)
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

            vacancy_dict = {
                "title": vacancy.title,
                "link": vacancy.link,
                "salary_from": vacancy.salary_from,
                "salary_to": vacancy.salary_to,
            }
            if vacancy_dict not in data:
                data.append(vacancy_dict)

            file.seek(0)
            file.truncate()
            json.dump(data, file, ensure_ascii=False, indent=4)

    def delete_data(self) -> None:
        pass
