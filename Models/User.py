'''
Модель пользователя для таблицы user базы данных
'''
from peewee import *
from Connection.connect import db
class User(Model):
    '''
    Поля таблицы user
    id, login, password,date_auth, bloked, role
    '''
    login = CharField(max_length=10, unique=True)
    password = CharField(max_length=255)
    date_auth = DateTimeField(null=True) # ПОЛЕ можно быть пустым
    bloked = BooleanField(default=False)
    role = CharField(max_length=20,choices=[
            ('admin', 'Администратор'),
            ('user', 'Пользователь'),

        ], default='user')
    class Meta:
        database = db
if __name__ == '__main__':
    db.create_tables([User])