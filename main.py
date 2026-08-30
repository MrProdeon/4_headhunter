from src.connector import HeadHunterApi
from src.FileWorker import JsonWorker
from utils.database_functions import database_vacancies_and_employers
from utils.functions import only_vacancies

hh_api = HeadHunterApi({"User-Agent": "test for skypro"})
json_worker = JsonWorker("data/json_data.json")


def main() -> None:
    while True:
        user_choise = ""
        while user_choise not in ("1", "2"):
            user_choise = input(
                """Каким сервисом хотите воспользоваться?
1 - Поиск вакансий с возможностью выбора критериев для поиска и записью информации в файл или консоль
2 - Поиск вакансий 10 топовых работодателей с записью в базу данных и получение данных из неё
Ваш выбор: """
            )

        if user_choise == "1":
            only_vacancies()
        elif user_choise == "2":
            database_vacancies_and_employers()

        is_work_end = ""
        while is_work_end not in ("1", "2"):
            is_work_end = input("Хотите воспользоваться другим сервисом? 1 - Да, 2 - Нет.")

        if is_work_end == "1":
            continue
        break


if __name__ == "__main__":
    main()
