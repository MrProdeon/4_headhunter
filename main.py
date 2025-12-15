from src.connector import Connector, HeadHunterApi
from utils.functions import ranged_vacancies, top_n, print_vacancies, dicts_to_objects, end_or_continue
from src.Vacancy import Vacancy
from src.FileWorker import JsonWorker

hh_api = HeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent" : "test for skypro"})
json_worker = JsonWorker("data/json_data.json")

def main():
    while True:
        try:
            target = sorted(list(map(int, input("""По каким критериям отфильтровать вакансии?
1 - ключевые слова
2 - по диапазону зарплат
3 - по самым высоким зарплатам
4 - удалёнка или офис
5 - просмотреть уже записанные вакансии из файла (если этот пункт будет выбран, то будет обработан только он)
(Напишите в одну строку через пробел)
""").strip().split())))
        except ValueError:
            continue
        if all(number in (1, 2, 3, 4, 5) for number in target):


            if 5 in target:
                target = 5
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
                    vacancies = [vacancy for vacancy in vacancies if
                                 any(work_format["id"] == "REMOTE" for work_format in vacancy["work_format"])]
                if work_f == "2":
                    vacancies = [vacancy for vacancy in vacancies if
                                 any(work_format["id"] == "ON_SITE" for work_format in vacancy["work_format"])]
                if work_f == "3":
                    vacancies = [vacancy for vacancy in vacancies if
                                 any(work_format["id"] == "HYBRID" for work_format in vacancy["work_format"])]


            vacancies = Vacancy.cast_to_object_list(vacancies)

            if 2 in target:
                while True:
                    range_from = input("Введите начальную зарплату: ")
                    range_to = input("Введите конечную зарплату: ")
                    try:
                        range_from = int(range_from)
                        range_to = int(range_to)
                        break
                    except ValueError:
                        print("Введите число!")
                        continue

                vacancies = ranged_vacancies(vacancies, range_from, range_to)

            if 3 in target:
                n = input("Какое отобразить количество вакансий с максимальной ЗП?  ")
                while True:
                    try:
                        n = int(n)
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





# Сделать перелистывание страницы







if __name__ == "__main__":
    main()