"""
Модуль контроллера пользователей.

Предоставляет статические методы для выполнения CRUD-операций
над моделью ``User``: создание, чтение, обновление и удаление записей,
а также аутентификацию пользователей.

Пример:
    >>> from Controllers.UserController import UserController
    >>> result = UserController.registration('new_user', 'password123')
    >>> print(result['message'])
"""
from Demo.Models.User import *  # type: ignore
from bcrypt import *


class UserController:
    """
    Контроллер для управления пользователями.

    Содержит набор статических методов, реализующих бизнес-логику
    работы с пользователями: регистрация, авторизация, получение списка,
    блокировка, обновление данных и удаление.

    Все методы возвращают словарь в формате:
        {'success': bool, 'message': str, 'user': User | None}
    """

    @staticmethod
    def registration(login: str, password: str, role: str = 'user') -> dict:
        """
        Регистрирует нового пользователя.

        Проверяет уникальность логина, хэширует пароль с помощью BCrypt
        и сохраняет запись в базе данных.

        Args:
            login: Уникальное имя пользователя.
            password: Пароль в открытом виде (будет зашифрован).
            role: Роль пользователя ('user' или 'admin'). По умолчанию 'user'.

        Returns:
            Словарь с результатом операции:
            - success (bool): ``True`` при успешном создании.
            - message (str): Сообщение о результате.
            - user (User | None): Созданный объект User или ``None`` при ошибке.
        """
        try:
            user = User.get_or_none(login=login)
            if user:
                return {'success': False, 'message': 'Такой логин уже занят', 'user': None}
            hash_password = hashpw(password.encode(), gensalt())
            user = User.create(login=login, password=hash_password, role=role)
            return {'success': True, 'message': 'Пользователь создан', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def auth(login: str, password: str) -> dict:
        """
        Аутентифицирует пользователя.

        Проверяет существование пользователя с указанным логином
        и корректность пароля (сравнение с хэшем BCrypt).

        Args:
            login: Логин пользователя.
            password: Пароль в открытом виде.

        Returns:
            Словарь с результатом:
            - success (bool): ``True`` при успешной аутентификации.
            - message (str): Сообщение о результате.
            - user (User | None): Объект пользователя или ``None``.
        """
        try:
            user = User.get_or_none(login=login)
            if user is None:
                return {'success': False, 'message': 'Вы ввели неверный логин или пароль.\nПожалуйста проверьте ещё раз введенные данные', 'user': None}

            if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return {'success': False, 'message': 'Вы ввели неверный логин или пароль.\nПожалуйста проверьте ещё раз введенные данные', 'user': None}
            return {'success': True, 'message': 'Вы успешно авторизовались', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def get():
        """
        Возвращает список всех пользователей.

        Выполняет запрос к таблице ``user`` и возвращает все записи.

        Returns:
            dict: Словарь с ключами:
            - success (bool): ``True`` при успешном получении данных.
            - message (str): Сообщение о результате.
            - users (list): Список объектов User.
        """
        try:
            users = User.select()
            return {'success': True, 'message': 'Вывод пользователей', 'users': users}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def blocked(id: int):
        """
        Блокирует пользователя по идентификатору.

        Args:
            id: Идентификатор пользователя.

        Returns:
            dict: Словарь с результатом операции.
        """
        pass  # метод пока не реализован

    @staticmethod
    def update(id: int, **fields: dict) -> dict:
        """
        Обновляет данные пользователя.

        Позволяет изменить произвольные поля пользователя.
        Если среди переданных полей есть ``password``, значение будет
        автоматически зашифровано с помощью BCrypt.

        Args:
            id: Идентификатор пользователя.
            **fields: Произвольные именованные аргументы — поля и их новые значения.
                      Например: ``login='new_login', password='new_password'``.

        Returns:
            dict: Словарь с результатом обновления.
        """
        try:
            user = User.get_or_none(id=id)
            for key, value in fields.items():
                if key == 'password':
                    value = hashpw(value.encode(), gensalt())
                User.update({key: value}).where(User.id == id).execute()
            return {'success': True, 'message': 'Пользователь обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def new_update(id: int, login: str = None, password: str = None,
                   blocked: bool = None, role: str = None) -> dict:
        """
        Обновляет данные пользователя с использованием именованных параметров.

        В отличие от ``update()``, принимает только явно указанные поля
        и не использует ``**kwargs``.

        Args:
            id: Идентификатор пользователя.
            login: Новый логин (или ``None``, если не изменяется).
            password: Новый пароль (или ``None``). Будет зашифрован.
            blocked: Новое состояние блокировки (или ``None``).
            role: Новая роль (или ``None``).

        Returns:
            dict: Словарь с результатом обновления.
        """
        try:
            update_data = {}
            if login:
                update_data['login'] = login
            if password:
                update_data['password'] = hashpw(password.encode(), gensalt())
            if blocked:
                update_data['blocked'] = blocked
            if role:
                update_data['role'] = role
            User.update(update_data).where(User.id == id).execute()
            user = User.get_by_id(id)
            return {'success': True, 'message': 'Пользователь обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def update_password(id: int, password: str) -> dict:
        """
        Обновляет пароль пользователя.

        Args:
            id: Идентификатор пользователя.
            password: Новый пароль в открытом виде (будет зашифрован).

        Returns:
            dict: Словарь с результатом операции.
        """
        try:
            User.update({'password': hashpw(password.encode(), gensalt())}).where(User.id == id).execute()
            user = User.get_by_id(id)
            return {'success': True, 'message': 'Пароль обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def delete(id: int):
        """
        Удаляет пользователя по идентификатору.

        Args:
            id: Идентификатор пользователя.

        Returns:
            dict: Словарь с результатом удаления.
        """
        try:
            User.delete().where(User.id == id).execute()
            return {'success': True, 'message': 'Пользователь удален', 'user': None}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}


if __name__ == '__main__':
    print("Тест создания пользователя")
    print(UserController().registration('admin', 'admin', 'admin'))
    print("Тест авторизации")
    print(UserController.auth('admin', 'admin'))
    print("Тест получения пользователей")
    for user in UserController.get()['users']:
        print(user.login, user.role, user.bloked)
    print("Тест обновления пользователя")
    print(UserController.update(1, login='user', password='user', role='admin', bloked=True))
    print("Тест снова обновления пользователя")
    print(UserController.new_update(1))
