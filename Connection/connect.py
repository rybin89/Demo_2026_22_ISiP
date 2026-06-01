'''
подключение к базе данных с помощью библиотеки peewee
'''
from peewee import *
db = MySQLDatabase(
    'rybin_demo',
    host='10.11.13.115',
    user='rybin',
    password='rybin',
    port=3306
    )

print(db.connect())