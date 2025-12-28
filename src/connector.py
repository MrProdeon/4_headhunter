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

    def get_employers(self, text : str = "", ):
        url = "https://api.hh.ru/employers"
        params = {"text" : text, "only_with_vacancies" : True, "page" : 0, "per_page" : 100}
        data = self._connect(params)


if __name__ == "__main__":

    # obj = HeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent": "test for skypro"})
    # obj_list = obj.get_vacancies("python")
    # print(json.dumps(obj_list, ensure_ascii=False, indent=4))

    obj = HeadHunterApi("https://api.hh.ru/employers", {"User-Agent": "test for skypro"})
    print(json.dumps(obj._connect({"per_page" : 100, "only_with_vacancies" : True}), ensure_ascii=False, indent=4))
