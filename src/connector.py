import json
import time
from abc import ABC, abstractmethod
from src.Vacancy import Vacancy

import requests
from typing import Any


class Connector(ABC):
    """Абстрактный класс для подключения к АПИ хедхантера."""

    @abstractmethod
    def _connect(self, params: dict, url) -> dict:
        pass

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        pass


class HeadHunterApi(Connector):
    """Класс для подключения к апи хедхантера.
    Имеет метод для get-подключения к апи, а так же метод именно для подключения к поиску вакансий
    с заданным текстом и страницей для поиска.
    """

    def __init__(self, headers: dict) -> None:
        self.__headers = headers

    def _connect(self, params: dict, url) -> Any:
        try:
            response = requests.get(url, headers=self.__headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HH API error: {e}")
            return None

    def get_vacancies(self, text: str = "", page: int = 0, employer_id=None) -> Any:
        url = "https://api.hh.ru/vacancies"
        full_data = []

        while True:
            time.sleep(0.5)

            params = {"text": text, "page": page, "per_page": 100, "only_with_salary": True}

            if employer_id:
                params["employer_id"] = employer_id

            data = self._connect(params, url)

            if not data:
                break

            searched_data = data.get("items", [])
            full_data.extend(searched_data)

            pages = data.get("pages")

            if pages is None:
                break

            if page < pages - 1:
                page += 1
            else:
                break

        return full_data

    def get_employers(self, text: str = ""):
        """
        Метод для получения желаемых работодателей. На данный момент работодатели зафиксированы в самом методе.
        Метод возвращает список списков, в котором каждый вложенный список - это искомые работодатели по их названию.
        """
        companies = [
            "Т-Банк",
            "Selectel",
            "X5 Tech",
            "Ozon Tech",
            "АВИТО ТЕХ",
            "Сбер Банк",
            "Альфа-Банк",
            "VK",
            "Kaspersky",
            "Skyeng",
        ]
        url = "https://api.hh.ru/employers"
        data = []

        for company in companies:
            params = {"text": f"{company}", "only_with_vacancies": True, "page": 0, "per_page": 100}
            response = self._connect(params, url)
            data.append(response["items"])

        return data

    @staticmethod
    def get_ids(companies: list):
        """Метод для получения айди компаний после того как был получен ответ от хедхантера об основной информации
        о компании.
        Вернет список словаей, где каждый словарь - айди компании и её название."""
        ids = []
        for i in companies:
            for j in i:
                ids.append({j["id"]: j["name"]})

        return ids
