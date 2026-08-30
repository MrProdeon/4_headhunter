import psycopg2
from psycopg2.extensions import connection
from typing import Any


class DBManager:
    """
    Класс для работы с базой данных, направлен на получение информации о работодателях и вакансиях.
    """

    def __init__(self, dbname : str, password : str, user: str = "postgres", host: str = "localhost", port: int = 5432) -> None:
        """
        Инициализация направлена на получение информации о базе данных, к которой
        будет происходить подключение.
        :param dbname: название базы данных, к которой происходит подключение
        :param password: пароль от базы данных
        :param user: имя пользователя базы данных
        :param host: название хоста для подключения к базе данных
        :param port: номер порта для подключения к базе данных
        """
        self.__dnname = dbname
        self.__password = password
        self.user = user
        self.host = host
        self.port = port

    def connect(self) -> connection:
        """
        Метод для получения коннекта к базе данных
        :return: объект коннекта с подключенной базой данных
        """
        conn = psycopg2.connect(
            dbname=self.__dnname, password=self.__password, user=self.user, host=self.host, port=self.port
        )
        return conn

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Метод для получения списка всех компаний и количества вакансий у каждой компании
        :return: список кортежей, где каждый кортеж - данные об одной строке в таблице
        """

        sql = """SELECT company_name, COUNT(vacancy_id) FROM employers
                 LEFT JOIN vacancies USING(employer_id)
                 GROUP BY company_name"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод для получения списка всех ваканий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return: список кортежей, где каждый кортеж - данные об одной строке в таблице
        """

        sql = """SELECT company_name, title, salary_from, salary_to, max_salary, url
         FROM vacancies
         JOIN employers USING(employer_id)
         """
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_avg_salary(self) -> Any:
        """
        Метод для получения средней зарплаты по вакансиям из таблицы со всеми вакансиями.
        :return: Число, которое является средней зарплатой по всем вакансиям из таблицы
        """

        sql = """SELECT ROUND(AVG(max_salary), 2) FROM vacancies"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchone()

                if result is None:
                    return None

                return result[0]

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получение вакансий с зарплатой, которая выше средней по всем вакансиям.
        :return:  список кортежей, где каждый кортеж - вакансия с ЗП выше средней.
        """
        sql = """SELECT company_name, title, salary_from, salary_to, url FROM vacancies
                 JOIN employers USING(employer_id)
                 WHERE max_salary > 
                 (SELECT AVG(max_salary) FROM vacancies)"""

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_vacancies_with_keyword(self, searched_word: str) -> list[tuple]:
        """Получение вакансий с поиском по ключевому слову
        :return: список кортежей, где каждый кортеж - вакансия с искомым ключевым словом.
        """
        sql = f"""SELECT company_name, title, salary_from, salary_to, url
                  FROM vacancies
                  JOIN employers USING(employer_id)
                  WHERE title ILIKE '%{searched_word}%'"""

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
