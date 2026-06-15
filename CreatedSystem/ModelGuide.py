# -*- coding: utf-8 -*-
'''
Руководство по созданию Модели в Peewee.

Данный модуль содержит подробное описание процесса создания
ORM-модели с использованием библиотеки Peewee на примере
модели User из проекта Demo.

---

## 1. Подключение базы данных

Прежде чем создавать модель, необходимо настроить подключение к базе данных.
В проекте Demo для этого используется модуль Connection.connect,
который создаёт глобальный объект db - экземпляр MySQLDatabase.

```python
from peewee import *

db = MySQLDatabase(
    'rybin_demo',
    host='127.127.126.26',
    user='root',
    password='',
    port=3306
)
```

Подробнее: Demo.Connection.connect

---

## 2. Импорты

Для создания модели Peewee необходимы следующие импорты:

```python
from peewee import *                          # ORM Peewee
from Demo.Connection.connect import db        # объект подключения к БД
```

---

## 3. Создание класса модели

Модель создается путём наследования от класса Model из Peewee.
Имя таблицы в базе данных по умолчанию соответствует имени класса
в нижнем регистре (для класса User - таблица user),
но может быть переопределено через Meta.

### 3.1. Определение полей

Каждое поле таблицы объявляется как атрибут класса с использованием
соответствующего типа поля Peewee:

- ``CharField`` - строковое поле (CharField(max_length=10))
- ``DateTimeField`` - дата и время (DateTimeField(null=True))
- ``BooleanField`` - логическое значение (BooleanField(default=False))
- ``IntegerField`` - целое число (IntegerField())
- ``ForeignKeyField`` - внешний ключ (ForeignKeyField(OtherModel))

### 3.2. Параметры полей

Поля могут принимать различные параметры:

- max_length - максимальная длина строки (для CharField).
- unique=True - уникальное значение (не может повторяться в таблице).
- null=True - поле может содержать None.
- default=value - значение по умолчанию.
- choices - список допустимых значений (для валидации).

### 3.3. Внутренний класс Meta

Внутренний класс Meta используется для конфигурации модели.
Основной атрибут - database, указывающий на объект подключения:

```python
class Meta:
    database = db
```

### 3.4. Полный пример модели User

Полный код модели User находится в модуле Demo.Models.User.

```python
from peewee import *
from Demo.Connection.connect import db


class User(Model):
    login = CharField(max_length=10, unique=True)
    password = CharField(max_length=255)
    date_auth = DateTimeField(null=True)
    bloked = BooleanField(default=False)
    role = CharField(
        max_length=20,
        choices=[
            ('admin', 'Администратор'),
            ('user', 'Пользователь'),
        ],
        default='user'
    )

    class Meta:
        database = db
```

---

## 4. Создание таблицы в базе данных

Чтобы физически создать таблицу в базе данных, используется
метод create_tables объекта подключения:

```python
if __name__ == '__main__':
    db.create_tables([User])
```

Этот код выполняется только при прямом запуске файла
(python Demo/Models/User.py) и создает таблицу user в БД.

---

## 5. Основные операции с моделью Peewee

### 5.1. Создание записи (Create)

```python
user = User.create(login='admin', password='hashed_pwd', role='admin')
```

### 5.2. Чтение записи (Read)

```python
# Получить по ID
user = User.get_by_id(1)

# Получить по условию или None
user = User.get_or_none(login='admin')

# Получить все записи
users = User.select()
```

### 5.3. Обновление записи (Update)

```python
User.update({field: value}).where(User.id == id).execute()
```

### 5.4. Удаление записи (Delete)

```python
User.delete().where(User.id == id).execute()
```

---

## 6. Поля модели User

- login (CharField): Логин пользователя. Уникальное значение, не более 10 символов.
- password (CharField): Пароль пользователя. Хранится в виде хэша BCrypt.
- date_auth (DateTimeField): Дата и время последней авторизации. Может быть None.
- bloked (BooleanField): Флаг блокировки пользователя.
- role (CharField): Роль пользователя. Допустимые значения: 'admin', 'user'.
'''

class UserModelExample:
    """
    Пример ORM-модели Peewee для документации.

    Этот класс демонстрирует структуру модели Peewee на примере User.
    Соответствует таблице user в базе данных.

    Attributes:
        login (str): Логин пользователя. Уникальное поле, не более 10 символов.
        password (str): Пароль пользователя. Хранится в виде хэша BCrypt.
        date_auth (str): Дата и время последней авторизации. Может быть None.
        bloked (bool): Флаг блокировки пользователя. True - заблокирован.
        role (str): Роль пользователя. Допустимые значения: 'admin', 'user'.
    """
    login: str = "admin"
    password: str = "hashed_password"
    date_auth: str = "2024-01-01 12:00:00"
    bloked: bool = False
    role: str = "user"


def create_tables_example():
    """
    Пример создания таблиц в базе данных.

    Используется метод db.create_tables([Model1, Model2, ...]),
    который создает таблицы для перечисленных моделей.

    Пример:
        >>> from Demo.Models.User import User
        >>> from Demo.Connection.connect import db
        >>> db.create_tables([User])

    Returns:
        None
    """
    pass


def create_record_example():
    """
    Пример создания записи (CREATE).

    Используется метод Model.create(...) для создания новой записи.

    Пример:
        >>> from Demo.Models.User import User
        >>> user = User.create(login='admin', password='hashed_pwd', role='admin')

    Returns:
        User: Созданный объект пользователя.
    """
    pass


def read_record_example():
    """
    Пример чтения записей (READ).

    Доступные методы:
    - User.get_by_id(id) - получить по идентификатору
    - User.get_or_none(condition) - получить по условию или None
    - User.select() - получить все записи

    Пример:
        >>> from Demo.Models.User import User
        >>> user = User.get_or_none(login='admin')
        >>> users = User.select()

    Returns:
        User | list: Объект пользователя или список пользователей.
    """
    pass


def update_record_example():
    """
    Пример обновления записи (UPDATE).

    Используется метод Model.update(...).where(...).execute().

    Пример:
        >>> from Demo.Models.User import User
        >>> User.update({'role': 'admin'}).where(User.id == 1).execute()

    Returns:
        None
    """
    pass


def delete_record_example():
    """
    Пример удаления записи (DELETE).

    Используется метод Model.delete().where(...).execute().

    Пример:
        >>> from Demo.Models.User import User
        >>> User.delete().where(User.id == 1).execute()

    Returns:
        None
    """
    pass


if __name__ == "__main__":
    print("Модуль-руководство по созданию Модели Peewee")
    print("Запустите pdoc для генерации HTML-документации")
