import os

import psycopg2
from src.connector import HeadHunterApi
from utils.functions import get_objects_with_employers
from dotenv import load_dotenv
from os import getenv

load_dotenv()
PASSWORD = os.getenv("DB_PASSOWRD")
DB_NAME = os.getenv("DB_NAME")

# СОЗДАНИЕ И ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ

conn = psycopg2.connect(
    dbname=DB_NAME,
    user="postgres",
    password=PASSWORD,
    host="localhost",
    port=5432
)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute("CREATE DATABASE headhunter")
except psycopg2.errors.DuplicateDatabase:
    print("База данных уже создана.")

my_conn = psycopg2.connect(
    dbname=DB_NAME,
    user="postgres",
    password=PASSWORD,
    host="localhost",
    port=5432
)
my_cur = my_conn.cursor()


my_cur.execute("CREATE TABLE IF NOT EXISTS employers (employer_id INT PRIMARY KEY, "
                "company_name VARCHAR(255), "
            "open_vacancies INT)")
my_conn.commit()

my_cur.execute("CREATE TABLE  IF NOT EXISTS vacancies (vacancy_id serial PRIMARY KEY, "
                "employer_id INT , "
                "employer_name VARCHAR(500), "
                "title VARCHAR(500), "
                "salary_from INT, "
                "salary_to INT, "
                "max_salary INT, "
                "url VARCHAR(500), "
                "CONSTRAINT fk_vacancies_employer FOREIGN KEY(employer_id) REFERENCES employers(employer_id))")
my_conn.commit()

obj = HeadHunterApi({"User-Agent": "test for skypro"})
employers = obj.get_employers()

employers_for_insert = []
for company in employers:
    for employer in company:
        employer_id = employer["id"]
        employer_name = employer["name"]
        open_vacancies = employer["open_vacancies"]
        employer_tuple = (employer_id, employer_name, open_vacancies)
        employers_for_insert.append(employer_tuple)

employers_objects = get_objects_with_employers(obj)

employers_objects_for_insert = []
for company_ in employers_objects:
    for employer_ in company_:
        employers_tuple = (employer_.employer_id, employer_.employer, employer_.title, employer_.salary_from,
                          employer_.salary_to, employer_.salary, employer_.link)
        employers_objects_for_insert.append(employers_tuple)

with my_conn:
    with my_cur:
        my_cur.executemany("INSERT INTO employers(employer_id, company_name, open_vacancies) VALUES (%s, %s, %s)", employers_for_insert)
        my_cur.executemany("INSERT INTO vacancies(employer_id, employer_name, "
                           "title, salary_from, salary_to, "
                           "max_salary, url) VALUES (%s, %s, %s, %s, %s, %s, %s)", employers_objects_for_insert)
