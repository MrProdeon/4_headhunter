import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="21Quaswexexort",
    host="localhost",
    port=5432
)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute("CREATE DATABASE headhunter")
except psycopg2.errors.DuplicateDatabase:
    print("База данных уже создана.")

conn = psycopg2.connect(
    dbname="headhunter",
    user="postgres",
    password="21Quaswexexort",
    host="localhost",
    port=5432
)
cur = conn.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS employers (employer_id INT PRIMARY KEY, "
                "company_name VARCHAR(255))")
conn.commit()



cur.execute("CREATE TABLE  IF NOT EXISTS vacancies (vacancy_id serial PRIMARY KEY, "
                "employer_id INT , "
                "url VARCHAR(500), "
                "CONSTRAINT fk_vacancies_employer FOREIGN KEY(employer_id) REFERENCES employers(employer_id))")
conn.commit()

conn.commit()
print('a')
