import psycopg2

class DBManager:

    def __init__(self, dbname, password, user: str = "postgres", host : str = "localhost", port : int = 5432):
        self.__dnname = dbname
        self.__password = password
        self.user = user
        self.host = host
        self.port = port

    def connect(self):
        """
        Метод для получения коннекта к базе данных
        :return: объект коннекта с подключенной базе данных
        """
        conn = psycopg2.connect(self.__dnname, self.__password, self.user, self.host, self.port)
        return conn

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass







