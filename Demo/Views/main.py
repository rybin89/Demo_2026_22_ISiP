"""
Модуль запуска приложения.

Точка входа в программу. Создаёт и запускает главное окно авторизации.

Пример:
    >>> python Views/main.py
"""
from Demo.Views.AuthView import *

window = AuthView()
window.mainloop()
