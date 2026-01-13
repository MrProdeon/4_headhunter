import psycopg2

class DBManager:
    """
    Класс для работы с базой данных, направлен на получение информации о работодателях и вакансиях.
    """

    def __init__(self, dbname, password, user: str = "postgres", host : str = "localhost", port : int = 5432):
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

    def connect(self):
        """
        Метод для получения коннекта к базе данных
        :return: объект коннекта с подключенной базой данных
        """
        conn = psycopg2.connect(dbname=self.__dnname,
                                password=self.__password,
                                user=self.user,
                                host=self.host,
                                port=self.port)
        return conn

    def get_companies_and_vacancies_count(self):
        """
        Метод для получения списка всех компаний и количества вакансий у каждой компании
        :return: список кортежей, где каждый кортеж - данные об одной строке в таблице
        """

        sql = """SELECT company_name, COUNT(*) FROM employers
        JOIN vacancies USING(employer_id)
        GROUP BY company_name"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_all_vacancies(self):
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



    def get_avg_salary(self):
        """
        Метод для получения средней зарплаты по вакансиям из таблицы со всеми вакансий.
        :return: Число, которое является средней зарплатой по всем вакансиям из таблицы
        """

        sql = """SELECT ROUND(AVG(max_salary), 2) FROM vacancies"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchone()
                return result[0]

    def get_vacancies_with_higher_salary(self):
        sql = """SELECT * FROM vacancies
        WHERE max_salary > 
        (SELECT AVG(max_salary) FROM vacancies)"""

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_vacancies_with_keyword(self, searched_word : str):
        sql = f"""SELECT *
                  FROM vacancies
                  WHERE title ILIKE '%{searched_word}%'"""

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()







