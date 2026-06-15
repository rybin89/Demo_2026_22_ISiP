"""
Модуль модели пользователя.

Определяет ORM-модель ``User`` для таблицы ``user`` в базе данных.
Использует Peewee для отображения таблицы на Python-класс.

Пример:
    >>> from Models.User import User
    >>> user = User.get_by_id(1)
    >>> print(user.login, user.role)

Attributes:
    User (Model): ORM-модель, соответствующая таблице ``user``.
        Поля:
        - id — первичный ключ (автоматически)
        - login — уникальное имя пользователя (до 10 символов)
        - password — хэш пароля (до 255 символов)
        - date_auth — дата последней авторизации (может быть None)
        - bloked — флаг блокировки (по умолчанию False)
        - role — роль пользователя: 'admin' / 'user' (по умолчанию 'user')
"""
from peewee import *
from Demo.Connection.connect import db


class User(Model):
    """
    ORM-модель пользователя.

    Соответствует таблице ``user`` в базе данных.
    Содержит поля для аутентификации, авторизации и управления доступом.

    Attributes:
        login (CharField): Логин пользователя, уникальный, макс. 10 символов.
        password (CharField): Пароль (хранится в виде хэша BCrypt), макс. 255 символов.
        date_auth (DateTimeField): Дата и время последней авторизации. Может быть ``None``.
        bloked (BooleanField): Флаг блокировки пользователя. ``True`` — заблокирован.
        role (CharField): Роль пользователя. Допустимые значения: 'admin', 'user'.
    """
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


if __name__ == '__main__':
    db.create_tables([User])
