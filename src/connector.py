from abc import ABC, abstractmethod
import requests
import json
from src.Vacancy import Vacancy

class Connector(ABC):

    """Абстрактный класс для подключения к АПИ хедхантера."""

    @abstractmethod
    def _connect(self, params):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass




class HeadHunterApi(Connector):

    """Класс для подключения к апи хедхантера.
    Имеет метод для get-подключения к апи, а так же метод именно для подключения к поиску вакансий
    с заданным текстом и страницей для поиска.
    """

    def __init__(self, url, headers):
        self.__url = url
        self.__headers = headers

    def _connect(self, params):
        try:
            response = requests.get(self.__url, headers=self.__headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            return {}

    def get_vacancies(self, text="", page=0):
        params = {"text" : text, "page" : page, "per_page" : 100}
        data = self._connect(params)
        return data.get("items", [])



if __name__ == "__main__":

    obj = HeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent" : "test for skypro"})
    obj_list = obj.get_vacancies("python")
    print(json.dumps(obj_list, ensure_ascii=False, indent=4))
