## Вакансии Хедхантера.

Консольное приложение для поиска и фильтрации вакансий через API HeadHunter. 

## Установка и использование:
1) Клонируйте репозиторий к себе на компьютер с помощью команды `git clone`
2) Проект использует poetry, поэтому для использования проекта установите его. И установите зависимости с помощью `poetry install`
3) Точка входа для работы с программой - main.py

# Функционал проекта:

# Пакет src

## Модуль connector

Модуль содержит абстрактный класс Connector и основной класс для работы
с апи хедхантера, который наследуется от абстрактного.

```class HeadHunterApi(Connector)```  
Класс для подключения к апи хедхантера.  
При инициализации принимает url и headers.

Методы класса:  

1) _connect(self, params)- используется для отправки запроса в хедхантер и получение  
информации в ответ. Информация сразу преобразуется в пайтон-объекты для удобства работы.  
В качестве аргумента принимает словарь параметров.

Пример использования:
```python
hh_api = HeadHunterApiHeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent" : "test for skypro"})
hh_api._connect({"text" : text, "page" : page, "per_page" : 100})
{
    'items': [
        {
            'id': '128692536',
            'premium': False,
            'name': 'Административный сотрудник в военный офис Посольства Республики Корея в РК',
            'department': None,
            'has_test': False,
            'response_letter_required': False,
            'area': {
                'id': '159',
                'name': 'Астана',
                'url': 'https://api.hh.ru/areas/159'
            },
            'salary': {
                'from': 1400,
                'to': None,
                'currency': 'USD',
                'gross': False
            },
            'salary_range': {
                'from': 1400,
                'to': None,
                'currency': 'USD',
                'gross': False
            },
            'mode': {
                'id': 'MONTH',
                'name': 'За месяц'
            },
            'frequency': {
                'id': 'MONTHLY',
                'name': 'Раз в месяц'
            },
            'type': {
                'id': 'open',
                'name': 'Открытая'
            },
            'address': {
                'city': 'Нур-Султан (Астана)',
                'street': 'микрорайон Юго-Восток (правая сторона), улица Обаган',
                'building': '5',
                'lat': 51.134633,
                'lng': 71.482073,
                'description': None,
                'raw': 'Нур-Султан (Астана), микрорайон Юго-Восток (правая сторона), улица Обаган, 5',
                'metro': None,
                'metro_stations': [],
                'id': '3881834'
            },
            'response_url': None,
            'sort_point_distance': None,
            'published_at': '2025-12-12T08:50:53+0300',
            'created_at': '2025-12-12T08:50:53+0300',
            'archived': False,
            'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=128692536',
            'show_logo_in_search': None,
            'show_contacts': True,
            'insider_interview': None,
            'url': 'https://api.hh.ru/vacancies/128692536?host=hh.ru',
            'alternate_url': 'https://hh.ru/vacancy/128692536',
            'relations': [],
            'employer': {
                'id': '593501',
                'name': 'Посольство Республики Корея в Республике Казахстан',
                'url': 'https://api.hh.ru/employers/593501',
                'alternate_url': 'https://hh.ru/employer/593501',
                'logo_urls': {
                    'original': 'https://img.hhcdn.ru/employer-logo-original-round/1104784.jpeg',
                    '90': 'https://img.hhcdn.ru/employer-logo-round/1104785.jpeg',
                    '240': 'https://img.hhcdn.ru/employer-logo-round/1104786.jpeg'
                },
                'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=593501',
                'country_id': 3,
                'accredited_it_employer': False,
                'trusted': True
            },
            'snippet': {
                'requirement': 'Наличие навыков владения компьютерными программами (Word, Excel, PowerPoint и т. д.). - Водительский стаж не менее 3 лет. - Степень бакалавра (или...',
                'responsibility': 'Поддержка деятельности Военного атташе. - Обеспечение управления служебным автомобилем военного офиса. - Координация и организация мероприятий и работы согласно протокола военного офиса.'
            },
            'contacts': None,
            'schedule': {
                'id': 'fullDay',
                'name': 'Полный день'
            },
            'working_days': [],
            'working_time_intervals': [],
            'working_time_modes': [],
            'accept_temporary': False,
            'fly_in_fly_out_duration': [],
            'work_format': [
                {'id': 'ON_SITE', 'name': 'На месте работодателя'}
            ],
            'working_hours': [
                {'id': 'HOURS_8', 'name': '8 часов'}
            ],
            'work_schedule_by_days': [
                {'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}
            ],
            'night_shifts': False,
            'professional_roles': [
                {'id': '76', 'name': 'Менеджер/руководитель АХО'}
            ],
            'accept_incomplete_resumes': False,
            'experience': {
                'id': 'between1And3',
                'name': 'От 1 года до 3 лет'
            },
            'employment': {
                'id': 'full',
                'name': 'Полная занятость'
            },
            'employment_form': {
                'id': 'FULL',
                'name': 'Полная'
            },
            'internship': False,
            'adv_response_url': None,
            'is_adv_vacancy': False,
            'adv_context': None
        }
    ]
}


```

2) get_vacancies(self, text="", page=0)
Метод именно для работы с вакансиями в апи хедхантера.  
Принимает аргументы для поиска ключевых слов и страниц, по умолчанию
поиск будет без ключевых слов и с нулевой страницы.  
Внутри метода вызывается метод _connect и формируется список словарей с вакансиями, на основе
ответа от хедхантера.  

Пример использования:
```python
obj = HeadHunterApi("https://api.hh.ru/vacancies", {"User-Agent" : "test for skypro"})
obj_list = obj.get_vacancies("python")
print(json.dumps(obj_list, ensure_ascii=False, indent=4))
>>>
[
    {
        "id": "128770812",
        "premium": false,
        "name": "Тестировщик (QA)",
        "department": null,
        "has_test": false,
        "response_letter_required": false,
        "area": {
            "id": "1",
            "name": "Москва",
            "url": "https://api.hh.ru/areas/1"
        }}]


```

## Модуль Vacancy

Модуль содержит в себе класс Vancy для работы с вакансиями.  
При инициализации принимает название, ссылку, начальную и конечную сумму ЗП.  
Имеет только эти слоты, больше не может принимать ничего другого.  
Имеет магические методы для справнения зарплат между объектами этого класса,
либо между объектом и числом. Сравнение происходит по свойству salary.

Черз property добавлено свойство зарплаты, которое ищет максимумальное число из
начальной и конечной зарплаты для корректного сравнения ЗП. По нему и идет сравнение, описанное выше.

При инициализации так же производится валидация с помощью внутренних методов
__validate_title и __validate_salary  

__Validate_title проверяет, что название указано и указано ли оно в виде строки.
Если нет - поставим в название строку "Без названия"  

__validate_salary проверяет передано ли число. Если число не передали, вернет 0.  


Класс содержит метод cast_to_object_list(vacancies: list[dict])  
Он нужен для преобразования данных, полученных по апи от хедхантера(список словарей) в список объектов класса Vacancy.


Пример использования:
```python

vacancies = [Vacancy("developer", "https", 80000, 100000),
             Vacancy("manager", "https", 60000, 80000)]

vacancies[0] > vacancies[1] >>> True
vacancies[0] <= vacancies[1] >>> False

vacancies[0].salary >>> 100000

vacancies_dict = {"name" : "developer", "alternate_url" : "https",
                  "salary_from" : 80000, "salary_to" : 100000}

obj_list = Vacancy.cast_to_object_list(vacancies_dict)
obj_list[0].title >>> "developer"
obj_list[0].link >>> "https"
obj_list[0].salary_from >>> 80000
obj_list[0].salary_to >>> 100000
obj_list[0].salary >>> 100000
```

## Модуль FileWorker

Имеет абстрактный класс FileWorker, который указывает методы, которые должны содержать его наследователи.  
А именно получение данных, запись данных и удаление данных.  


Класс JsonWorker  
Класс для работы с JSON-файлами.  
При инициализации принимает путь до файла, в котором имеются данные для чтения и в который будем записывать новые данные.  
Если файл не передать, есть значение по умолчанию "data/json_data.json"

Методы:  

### get_data

Производится попытка открыть переданный JSON-файл.  
Если попытка завершилась успешно, преобразует данные в пайтон-код и вернет эти данные.  
Если файл оказался пустым, то вернет пустой список.  
А так же вернет пустой список, если файла не указалось.  

Пример использования:
```python

json_worker = JsonWorker()
json_worker.get_data()
>>> 
[
    {
        "title": "Data Engineer/Дата инженер (Junior)",
        "link": "https://hh.ru/vacancy/127891259",
        "salary_from": 0,
        "salary_to": 100000
    }]
```


### add_data

Изначально открываем файл, если он уже есть. Если нет - он будет создан.  
Читаем данные из этого файла, если они есть, а если нет - делаем пустой список.  
Формируется словарь на основе переданного объекта класса Vacancy и проверяется
нет ли такого же словаря в файле. Если есть - он не будет добавлен.  
После проверки вакансия добавляется и список и список записывается в файл.  

Пример  использования:
```python
json_worker = JsonWorker()
json_worker.add_data(Vacancy("developer", "https", 80000, 100000))
>>>
В файл "data/json_data.json" будет добавлен словарь:
{
    "title" : "developer",
    "link" : "https",
    "salary_from" : 80000,
    "salary_to" : 10000
}


```

### delete_data
На данный момент метод не реализован.


# Пакет utils

## Модуль functions
В этом модуле написаны вспомогательные функции для работы программы.

### def top_n(vacancies : list[Vacancy], n : int)  
Функция для отображения топовых зарплат по вакансиям.  
На вход принимает список с объектами вакансий и число n, которое указывает на кол-во
желаемого получения зарплат.  
В функции производится сортировка пузырьком в обратном порядке, то есть сначала будет идти
наибольшие суммы, а в конце наименьшие.

Пример использования:
```python
vacancies = [Vacancy("developer", "https", 80000, 100000),
             Vacancy("manager", "https", 60000, 80000)]

result = top_n(vacancies, 1)
>>>
result[0].title >>> "developer"
result[0].salary >>> 100000
```

### def ranged_vacancies(vacancies : list[Vacancy], range_from : int | float, range_to : int | float = None)  
Функция для отображения вакансий в выбранном диапазоне зарплат.  
Принимает на вход список с объектами вакансий, от какой и до какой суммы искать.  
Производит поиск и возвращает список с нужными вакансиями.  

Пример использования:
```python
vacancies = [Vacancy("developer", "https", 80000, 100000),
             Vacancy("manager", "https", 60000, 80000)]

result = randeg_vacancies(vacancies, 90000, 110000)
len(result) >>> 1
result[0].title >>> "developer"


```

### def print_vacancies(vacancies : list[Vacancy]) -> str
Функция для форматирования списка объектов вакансий в строку и последующий вывод этой строки.
Принимает на вход список с объектами вакансий и формирует одну большую строчку с переносами строки.
После формирования выводит её.

Пример испрользования:
```python
vacancies = [Vacancy("developer", "https", 80000, 100000)]


print_vacancies(vacancies)
>>> "developer От: 80000, до 100000 https"
```

### def dicts_to_objects(vacancies : list[dict])
Функция для формирования списка объектов после чтения файла, в который уже добавлялись записи.  
В JSON-файл добавляется иной формат словарей, из-за чего и требуется дополнительная функция для их форматирования.  

Пример использования:
```python

json_worker = JsonWorker()
data = json_worker.get_data()
>>>
[
    {
        "title": "Data Engineer/Дата инженер (Junior)",
        "link": "https://hh.ru/vacancy/127891259",
        "salary_from": 0,
        "salary_to": 100000
    }]

result = dicts_to_objects(data)
>>>
result[0].title >>> "Data Engineer/Дата инженер (Junior)"
result.salary_from >>> 0

```

### end_or_continue()
Функция для основной программы, с помощью которой решается продолжить ли
работа или завершить программу
Пользователь вводит 1 или 2  
Если 1 - программа начинается снова  
Если 2 - программа завершется

# Тесты 

Для всех модулей проекта были написаны тесты с помощью pytest

# Документация и ссылки

Документация hh.ru - https://api.hh.ru/openapi/redoc#section/Obshaya-informaciya

Документация по поиску вакансий - https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies

url для поиска вакансий - https://api.hh.ru/vacancies

# Лицензия

На данный момент у проекта нет лицензии















