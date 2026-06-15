"""
Модуль подключения к базе данных.

Использует библиотеку Peewee для подключения к MySQL.
Создаёт глобальный объект подключения ``db``,
который импортируется в других модулях проекта.

Пример:
    >>> from Connection.connect import db
    >>> db.connect()

Attributes:
    db (MySQLDatabase): Объект подключения к базе данных MySQL.
        Параметры подключения:
        - database: rybin_demo
        - host: 127.127.126.26
        - user: root
        - password: (пустой)
        - port: 3306
"""
from peewee import *

db = MySQLDatabase(
    'rybin_demo',
    host='127.127.126.26',
    user='root',
    password='',
    port=3306
)

print(db.connect())
