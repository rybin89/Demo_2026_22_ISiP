# -*- coding: utf-8 -*-
'''
Руководство по созданию Контроллера с CRUD-методами.

Данный модуль содержит подробное описание процесса создания
контроллера, реализующего CRUD-операции (Create, Read, Update, Delete)
с использованием ORM Peewee на примере контроллера UserController
из проекта Demo.

---

## 1. Что такое Контроллер?

Контроллер - это класс, который содержит бизнес-логику приложения
и выступает промежуточным звеном между моделью (данными) и представлением
(пользовательским интерфейсом). Он инкапсулирует операции над моделью
и предоставляет единый интерфейс для работы с данными.

В проекте Demo контроллеры реализованы как классы со статическими методами,
что позволяет вызывать их без создания экземпляра класса.

---

## 2. Базовая структура контроллера

### 2.1. Импорты

```python
from Demo.Models.User import *   # Импорт модели User
from bcrypt import *             # Библиотека для хэширования паролей
```

### 2.2. Формат возвращаемых данных

Все методы контроллера возвращают словарь (dict) в едином формате:

```python
{
    'success': bool,      # True - операция успешна, False - ошибка
    'message': str,       # Текстовое сообщение о результате
    'user': User | None,  # Объект модели или None
}
```

### 2.3. Обработка ошибок

Каждый метод использует блок try / except Exception для перехвата
исключений и возврата корректного сообщения об ошибке:

```python
try:
    # ... код операции ...
    return {'success': True, 'message': '...', 'user': ...}
except Exception as e:
    return {'success': False, 'message': e, 'user': None}
```

---

## 3. CRUD-операции (Create, Read, Update, Delete)

### 3.1. CREATE - Создание записи (registration)

Метод создает нового пользователя в базе данных.

Алгоритм работы:
1. Проверка уникальности логина (User.get_or_none(login=login)).
2. Хэширование пароля с помощью BCrypt (hashpw + gensalt).
3. Создание записи через User.create(...).

```python
@staticmethod
def registration(login: str, password: str, role: str = 'user') -> dict:
    try:
        user = User.get_or_none(login=login)
        if user:
            return {'success': False, 'message': 'Такой логин уже занят', 'user': None}
        hash_password = hashpw(password.encode(), gensalt())
        user = User.create(login=login, password=hash_password, role=role)
        return {'success': True, 'message': 'Пользователь создан', 'user': user}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

---

### 3.2. READ - Чтение записей

#### 3.2.1. Аутентификация (auth)

Проверяет логин и пароль пользователя.

Алгоритм работы:
1. Поиск пользователя по логину.
2. Если пользователь не найден - возврат ошибки.
3. Сравнение пароля с хэшем BCrypt (checkpw).

```python
@staticmethod
def auth(login: str, password: str) -> dict:
    try:
        user = User.get_or_none(login=login)
        if user is None:
            return {'success': False, 'message': 'Неверный логин или пароль', 'user': None}
        if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {'success': False, 'message': 'Неверный логин или пароль', 'user': None}
        return {'success': True, 'message': 'Вы успешно авторизовались', 'user': user}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

#### 3.2.2. Получение списка (get)

Возвращает всех пользователей из базы данных.

```python
@staticmethod
def get():
    try:
        users = User.select()
        return {'success': True, 'message': 'Вывод пользователей', 'users': users}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

---

### 3.3. UPDATE - Обновление записи

#### 3.3.1. Обновление произвольных полей (update)

Метод принимает **kwargs и обновляет указанные поля пользователя.
Если среди полей есть password - значение автоматически хэшируется.

```python
@staticmethod
def update(id: int, **fields: dict) -> dict:
    try:
        user = User.get_or_none(id=id)
        for key, value in fields.items():
            if key == 'password':
                value = hashpw(value.encode(), gensalt())
            User.update({key: value}).where(User.id == id).execute()
        return {'success': True, 'message': 'Пользователь обновлен', 'user': user}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

#### 3.3.2. Обновление с именованными параметрами (new_update)

Альтернативный метод, принимающий только явно указанные поля.

```python
@staticmethod
def new_update(id: int, login: str = None, password: str = None,
               blocked: bool = None, role: str = None) -> dict:
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
```

#### 3.3.3. Обновление пароля (update_password)

Специализированный метод для смены пароля.

```python
@staticmethod
def update_password(id: int, password: str) -> dict:
    try:
        User.update({'password': hashpw(password.encode(), gensalt())}).where(User.id == id).execute()
        user = User.get_by_id(id)
        return {'success': True, 'message': 'Пароль обновлен', 'user': user}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

---

### 3.4. DELETE - Удаление записи (delete)

Удаляет пользователя по идентификатору.

```python
@staticmethod
def delete(id: int):
    try:
        User.delete().where(User.id == id).execute()
        return {'success': True, 'message': 'Пользователь удален', 'user': None}
    except Exception as e:
        return {'success': False, 'message': e, 'user': None}
```

---

## 4. Сводная таблица CRUD-методов

- **CREATE** - registration() - Создание нового пользователя
- **READ** - auth() - Аутентификация (чтение одной записи)
- **READ** - get() - Получение списка всех пользователей
- **UPDATE** - update() - Обновление произвольных полей
- **UPDATE** - new_update() - Обновление явно указанных полей
- **UPDATE** - update_password() - Смена пароля
- **DELETE** - delete() - Удаление пользователя

---

## 5. Рекомендации по созданию контроллера

1. **Единый формат ответа.** Все методы возвращают словарь с ключами
   success, message и данными. Это упрощает обработку результатов
   на стороне представления.

2. **Обработка ошибок.** Используйте try / except для перехвата
   исключений базы данных и возврата понятного сообщения пользователю.

3. **Безопасность паролей.** Никогда не храните пароли в открытом виде.
   Используйте BCrypt (или аналогичный алгоритм) для хэширования.

4. **Статические методы.** Статические методы не требуют создания
   экземпляра класса, что делает их удобными для вызова из любой точки
   приложения.

5. **Типизация.** Используйте аннотации типов для улучшения
   читаемости кода и автодополнения в IDE.

---

## 6. Полный код контроллера UserController

Полный исходный код находится в модуле Demo.Controllers.UserController.
'''

class UserControllerExample:
    """
    Пример контроллера с CRUD-методами для документации pdoc.

    Этот класс дублирует структуру Demo.Controllers.UserController
    для того, чтобы pdoc сгенерировал читаемую документацию.

    Контроллер реализует следующие CRUD-операции:
        - Create: registration
        - Read: auth, get
        - Update: update, new_update, update_password
        - Delete: delete
    """

    @staticmethod
    def registration(login: str, password: str, role: str = 'user') -> dict:
        """
        Регистрирует нового пользователя (CREATE).

        Проверяет уникальность логина, хэширует пароль с помощью BCrypt
        и сохраняет запись в базе данных.

        Args:
            login: Уникальное имя пользователя.
            password: Пароль в открытом виде (будет зашифрован).
            role: Роль пользователя ('user' или 'admin'). По умолчанию 'user'.

        Returns:
            Словарь с результатом операции:
            - success (bool): True при успешном создании.
            - message (str): Сообщение о результате.
            - user (User | None): Созданный объект User или None при ошибке.
        """
        ...

    @staticmethod
    def auth(login: str, password: str) -> dict:
        """
        Аутентифицирует пользователя (READ).

        Проверяет существование пользователя с указанным логином
        и корректность пароля (сравнение с хэшем BCrypt).

        Args:
            login: Логин пользователя.
            password: Пароль в открытом виде.

        Returns:
            Словарь с результатом:
            - success (bool): True при успешной аутентификации.
            - message (str): Сообщение о результате.
            - user (User | None): Объект пользователя или None.
        """
        ...

    @staticmethod
    def get() -> dict:
        """
        Возвращает список всех пользователей (READ).

        Выполняет запрос к таблице user и возвращает все записи.

        Returns:
            Словарь с ключами:
            - success (bool): True при успешном получении данных.
            - message (str): Сообщение о результате.
            - users (list): Список объектов User.
        """
        ...

    @staticmethod
    def update(id: int, **fields) -> dict:
        """
        Обновляет данные пользователя (UPDATE).

        Позволяет изменить произвольные поля пользователя.
        Если среди переданных полей есть password, значение будет
        автоматически зашифровано с помощью BCrypt.

        Args:
            id: Идентификатор пользователя.
            **fields: Произвольные именованные аргументы - поля и их новые значения.

        Returns:
            Словарь с результатом обновления:
            - success (bool): True при успешном обновлении.
            - message (str): Сообщение о результате.
            - user (User | None): Обновленный объект User.
        """
        ...

    @staticmethod
    def new_update(id: int, login: str = None, password: str = None,
                   blocked: bool = None, role: str = None) -> dict:
        """
        Обновляет данные пользователя с использованием именованных параметров (UPDATE).

        В отличие от update(), принимает только явно указанные поля
        и не использует **kwargs.

        Args:
            id: Идентификатор пользователя.
            login: Новый логин (или None, если не изменяется).
            password: Новый пароль (или None). Будет зашифрован.
            blocked: Новое состояние блокировки (или None).
            role: Новая роль (или None).

        Returns:
            Словарь с результатом обновления.
        """
        ...

    @staticmethod
    def update_password(id: int, password: str) -> dict:
        """
        Обновляет пароль пользователя (UPDATE).

        Args:
            id: Идентификатор пользователя.
            password: Новый пароль в открытом виде (будет зашифрован).

        Returns:
            dict: Словарь с результатом операции.
        """
        ...

    @staticmethod
    def delete(id: int) -> dict:
        """
        Удаляет пользователя по идентификатору (DELETE).

        Args:
            id: Идентификатор пользователя.

        Returns:
            dict: Словарь с результатом удаления.
        """
        ...


if __name__ == "__main__":
    print("Модуль-руководство по созданию Контроллера с CRUD-методами")
    print("Запустите pdoc для генерации HTML-документации")
