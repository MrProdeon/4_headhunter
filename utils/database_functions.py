from os import getenv

import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv

from src.connector import HeadHunterApi
from src.DBManager import DBManager
from utils.functions import end_or_continue, get_objects_with_employers

load_dotenv()
PASSWORD = getenv("DB_PASSOWRD", "postgres")
DB_NAME = getenv("DB_NAME", "postgres")

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


def create_database() -> None:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password=PASSWORD, host="localhost", port=5432)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute("CREATE DATABASE headhunter")
        print("Создание базы данных...")
    except psycopg2.errors.DuplicateDatabase:
        print("База данных уже создана...")


def get_connection() -> connection:
    return psycopg2.connect(dbname=DB_NAME, user="postgres", password=PASSWORD, host="localhost", port=5432)


def create_tables() -> None:
    print("Приступаем к созданию таблиц. Ожидайте...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS employers (employer_id INT PRIMARY KEY, " "company_name VARCHAR(255))"
            )
            print("Таблица работодателей создана.")

            cur.execute(
                "CREATE TABLE  IF NOT EXISTS vacancies (vacancy_id serial PRIMARY KEY, "
                "employer_id INT , "
                "title VARCHAR(500), "
                "salary_from INT, "
                "salary_to INT, "
                "max_salary INT, "
                "url VARCHAR(500) UNIQUE, "
                "CONSTRAINT fk_vacancies_employer FOREIGN KEY(employer_id) REFERENCES employers(employer_id))"
            )
            print("Таблица вакансий создана")
    print("Таблицы успешно созданы.")


def insert_database() -> None:
    print("Приступаем к получению данных о работодателях. Ожидайте...")
    obj = HeadHunterApi({"User-Agent": "test for skypro"})
    employers = obj.get_employers(companies)

    employers_for_insert = []
    for company in employers:
        for employer in company:
            employer_id = employer["id"]
            employer_name = employer["name"]
            employer_tuple = (employer_id, employer_name)
            employers_for_insert.append(employer_tuple)
    print("Данные о работодателях получены")

    print("Приступаем к получению данных о вакансиях.")
    employers_objects = get_objects_with_employers(obj)

    employers_objects_for_insert = []
    for company_ in employers_objects:
        for employer_ in company_:
            employers_tuple = (
                employer_.employer_id,
                employer_.title,
                employer_.salary_from,
                employer_.salary_to,
                employer_.salary,
                employer_.link,
            )
            employers_objects_for_insert.append(employers_tuple)
    print("Данные о вакансиях получены")

    print("Начинаем заполнение таблиц. Ожидайте...")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO employers(employer_id, company_name)"
                " VALUES (%s, %s) "
                "ON CONFLICT (employer_id) DO NOTHING",
                employers_for_insert,
            )
            cur.executemany(
                "INSERT INTO vacancies(employer_id, "
                "title, salary_from, salary_to, "
                "max_salary, url) VALUES (%s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (url) DO UPDATE SET "
                "title = EXCLUDED.title, "
                "salary_from = EXCLUDED.salary_from, "
                "salary_to = EXCLUDED.salary_to, "
                "max_salary = EXCLUDED.max_salary",
                employers_objects_for_insert,
            )


headhunter_db = DBManager(DB_NAME, PASSWORD)


def database_vacancies_and_employers() -> None: # pragma: no cover
    print("Вы выбрали работу с базой данных. Для её создания и заполнения требуется больше времени. Ожидайте.")

    print("Таблицы успешно заполнены.")
    while True:
        try:
            target = sorted(
                list(
                    map(
                        int,
                        input(
                            """Какие данные хотите получить?
1 - получить список всех компаний и количество вакансий у каждой из них.
2 - список всех ваканий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3 - получение средней зарплаты по всем вакансиям.
4 - Получение вакансий с зарплатой, которая выше средней по всем вакансиям в базе данных.
5 - Получение вакансий с поиском по ключевому слову
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
            pass

        if 1 in target:
            result = headhunter_db.get_companies_and_vacancies_count()
            for employer, count_vacacnies in result:
                print(employer, count_vacacnies)
            print("=" * 40)
        if 2 in target:
            result = headhunter_db.get_all_vacancies()
            for employer, title, salary_from, salary_to, max_salary, url in result:
                print(f"Работодатель - {employer}")
                print(f"Название вакансии - {title}")
                print(f"Зарплата от - {salary_from}")
                print(f"Зарплата до - {salary_to}")
                print(f"Ссылка на вакансию - {url}")
                print("-" * 40)
        if 3 in target:
            result = headhunter_db.get_avg_salary()
            print(result)
            print("=" * 40)
        if 4 in target:
            result = headhunter_db.get_vacancies_with_higher_salary()
            for employer, title, salary_from, salary_to, url in result:
                print(f"Работодатель - {employer}")
                print(f"Название вакансии - {title}")
                print(f"Зарплата от - {salary_from}")
                print(f"Зарплата до - {salary_to}")
                print(f"Ссылка на вакансию - {url}")
                print("-" * 40)
            print("=" * 40)
        if 5 in target:
            keyword = input("Введите ключевое слово для поиска в вакансиях: ")
            result = headhunter_db.get_vacancies_with_keyword(keyword)
            for employer, title, salary_from, salary_to, url in result:
                print(f"Работодатель - {employer}")
                print(f"Название вакансии - {title}")
                print(f"Зарплата от - {salary_from}")
                print(f"Зарплата до - {salary_to}")
                print(f"Ссылка на вакансию - {url}")
                print("-" * 40)
            print("=" * 40)

        if end_or_continue():
            continue
        break
