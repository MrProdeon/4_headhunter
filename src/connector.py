import json
from abc import ABC, abstractmethod

import requests
from typing import Any


class Connector(ABC):
    """Абстрактный класс для подключения к АПИ хедхантера."""

    @abstractmethod
    def _connect(self, params : dict, url) -> dict:
        pass

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        pass


class HeadHunterApi(Connector):
    """Класс для подключения к апи хедхантера.
    Имеет метод для get-подключения к апи, а так же метод именно для подключения к поиску вакансий
    с заданным текстом и страницей для поиска.
    """

    def __init__(self, headers : dict) -> None:
        self.__headers = headers

    def _connect(self, params : dict, url) -> Any:
        try:
            response = requests.get(url, headers=self.__headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            return {}

    def get_vacancies(self, text :str = "", page : int = 0) -> Any:
        url = "https://api.hh.ru/vacancies"
        params = {"text": text, "page": page, "per_page": 100}
        data = self._connect(params, url)
        return data.get("items", [])

    def get_employers(self, text : str = ""):
        """
        Метод для получения желаемых работодателей. На данный момент работодатели зафиксированы в самом методе.
        Метод возвращает список списков, в котором каждый вложенный список - это искомые работодатели по их названию.
        """
        companies = ["Т-Банк", "Selectel", "X5 Tech", "Ozon Tech", "АВИТО ТЕХ", "Сбер Банк", "Альфа-Банк", "VK", "Kaspersky", "Skyeng"]
        url = "https://api.hh.ru/employers"
        data = []

        for company in companies:
            params = {"text" : f"{company}", "only_with_vacancies" : True, "page" : 0, "per_page" : 100}
            response = self._connect(params, url)
            data.append(response["items"])

        return data

    @staticmethod
    def get_ids(companies : list):
        """Метод для получения айди компаний после того как был получен ответ от хедхантера об основной информации
        о компании.
        Вернет список словаей, где каждый словарь - айди компании и её название."""
        ids = []
        for i in companies:
            for j in i:
                ids.append({j["id"] : j["name"]})

        return ids



if __name__ == "__main__":

    # obj = HeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent": "test for skypro"})
    # obj_list = obj.get_vacancies("python")
    # print(json.dumps(obj_list, ensure_ascii=False, indent=4))

    obj = HeadHunterApi({"User-Agent": "test for skypro"})

    print(obj.get_employers())
