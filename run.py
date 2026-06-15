"""
Точка входа в приложение Demo.

Запускает главное окно авторизации из пакета Demo.

Пример:
    >>> python run.py
"""
from Demo.Views.main import *


if __name__ == '__main__':
    window = AuthView()
    window.mainloop()
