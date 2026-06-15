"""
Пакет документации по созданию Модели Peewee и Контроллера с CRUD-методами.

Содержит подробное описание процесса создания ORM-модели с использованием
библиотеки Peewee и Контроллера, реализующего базовые CRUD-операции:
Create (Создание), Read (Чтение), Update (Обновление), Delete (Удаление).

## Модули

- **ModelGuide** — руководство по созданию Модели в Peewee:
    Определение полей модели (CharField, IntegerField, DateTimeField, BooleanField),
    настройка Meta-класса (database, table_name), создание таблицы (create_table,
    create_tables), методы работы с записями (Post, Get, Delete).

- **ControllerGuide** — руководство по созданию Контроллера с CRUD-методами:
    Класс контроллера с методами: auth (аутентификация), registration (CREATE),
    get (READ), update/new_update (UPDATE), delete (DELETE). Обработка ошибок,
    хеширование паролей (bcrypt), возврат словарей с полями 'success', 'message', 'user'.

- **ViewGuide** — руководство по Tkinter окнам для управления записями БД:
    AuthView (авторизация), AdminView (создание + таблица), EditUser (редактирование),
    Puzzl_1 (капча-пазл для защиты от ботов), ModApi (валидация данных из API).

## Установка необходимых библиотек

Для работы проекта Demo и генерации документации требуется установить
следующие библиотеки. Все они находятся в папке ``my_packages/``.

### Основные библиотеки проекта

| Библиотека       | Назначение                          | Файл .whl                             |
|------------------|-------------------------------------|---------------------------------------|
| peewee           | ORM для работы с БД MySQL           | peewee-4.0.8-py3-none-any.whl         |
| pymysql          | Драйвер MySQL для Python            | pymysql-1.2.0-py3-none-any.whl        |
| bcrypt           | Хеширование паролей                 | bcrypt-5.0.0-cp39-abi3-win_amd64.whl  |
| requests         | HTTP-запросы к API                  | requests-2.34.2-py3-none-any.whl      |
| pillow           | Обработка изображений (капча)       | pillow-12.2.0-cp312-cp312-win_amd64.whl |
| python-docx      | Работа с DOCX-файлами               | python_docx-1.2.0-py3-none-any.whl    |

### Библиотеки для документации

| Библиотека       | Назначение                          | Файл .whl                             |
|------------------|-------------------------------------|---------------------------------------|
| pdoc             | Генерация HTML-документации         | pdoc-16.0.0-py3-none-any.whl          |
| jinja2           | Шаблонизатор (зависимость pdoc)     | jinja2-3.1.6-py3-none-any.whl         |
| markupsafe       | Безопасное экранирование (зависимость) | markupsafe-3.0.3-cp312-cp312-win_amd64.whl |
| pygments         | Подсветка кода (зависимость pdoc)   | pygments-2.20.0-py3-none-any.whl      |
| markdown2        | Разметка Markdown (зависимость pdoc)| markdown2-2.5.5-py3-none-any.whl      |

### Дополнительные зависимости

| Библиотека       | Назначение                          | Файл .whl                             |
|------------------|-------------------------------------|---------------------------------------|
| certifi          | SSL-сертификаты (зависимость requests) | certifi-2026.5.20-py3-none-any.whl  |
| charset-normalizer | Кодировки (зависимость requests)   | charset_normalizer-3.4.7-cp312-cp312-win_amd64.whl |
| idna             | IDNA-обработка (зависимость requests) | idna-3.18-py3-none-any.whl          |
| urllib3          | HTTP-клиент (зависимость requests)  | urllib3-2.7.0-py3-none-any.whl        |
| typing-extensions | Типизация (зависимость)             | typing_extensions-4.15.0-py3-none-any.whl |
| lxml             | XML-обработка (зависимость python-docx) | lxml-6.1.1-cp312-cp312-win_amd64.whl |

### Команды для установки

Все библиотеки собраны в файле ``my_packages/requirements-docs.txt``.
Для установки выполните:

```bash
# Активировать виртуальное окружение
.venv\\Scripts\\activate

# Установка всех библиотек из папки my_packages
pip install --no-index --find-links my_packages -r requirements.txt

# Или установка конкретных библиотек:
pip install --no-index --find-links my_packages peewee bcrypt pymysql requests pillow python-docx
pip install --no-index --find-links my_packages pdoc jinja2 markupsafe pygments markdown2
```

Либо через виртуальное окружение проекта:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install --no-index --find-links my_packages -r requirements.txt
```

### Проверка установки

После установки проверьте, что все библиотеки импортируются:

```bash
python -c "import peewee; import pymysql; import bcrypt; import requests; print('OK')"
python -c "import pdoc; import jinja2; import PIL; from docx import Document; print('OK')"
```

---

## Процесс создания документации

Документация в формате pdoc создаётся из Python-модулей пакета ``CreatedSystem``,
содержащих подробные docstring в формате Markdown.

### Этапы создания:

1. **Написание модулей-руководств**: Создаются файлы ``ModelGuide.py``,
   ``ControllerGuide.py``, ``ViewGuide.py`` в папке ``CreatedSystem/``.
   Каждый модуль содержит docstring с описанием архитектуры, примерами кода,
   таблицами и пошаговыми инструкциями.

2. **Генерация HTML**: Из корня проекта выполняется команда:
   ```
   python -m pdoc --output-dir CreatedSystem/docs CreatedSystem
   ```
   pdoc анализирует docstring модулей и создаёт HTML-файлы:
   - ``index.html`` — главная страница документации
   - ``CreatedSystem.html`` — описание пакета (содержимое ``__init__.py``)
   - ``CreatedSystem/ModelGuide.html`` — руководство по Модели
   - ``CreatedSystem/ControllerGuide.html`` — руководство по Контроллеру
   - ``CreatedSystem/ViewGuide.html`` — руководство по Представлениям

3. **Проверка и обновление**: После изменения содержимого любого модуля
   команда pdoc запускается повторно для перегенерации HTML-документации.

### Требования к окружению

Для генерации документации необходимы:
- Python 3.9+
- Библиотека pdoc (установлена в my_packages)
- Активированное виртуальное окружение (.venv)
"""
