"""
Модуль окна авторизации.

Предоставляет графический интерфейс для входа пользователя в систему.
Использует библиотеку Tkinter для построения интерфейса.

Пример:
    >>> from Views.AuthView import AuthView
    >>> window = AuthView()
    >>> window.mainloop()
"""
from tkinter import *
from tkinter import ttk

from Demo.Controllers.UserController import UserController



class AuthView(Tk):
    """
    Окно авторизации пользователя.

    Содержит поля для ввода логина и пароля, а также кнопку для входа.
    При успешной аутентификации пользователя с ролью 'admin' открывает
    панель администратора (AdminView).

    Attributes:
        title (str): Заголовок окна — 'Авторизация'.
        geometry (str): Размер окна — 800x800 пикселей.
        login_entry (Entry): Поле ввода логина.
        password_entry (Entry): Поле ввода пароля.
        login_message (Label): Метка для вывода сообщений о результате входа.
    """
    def __init__(self):
        """Инициализирует окно авторизации и все его элементы."""
        super().__init__()

        self.title('Авторизация')
        self.geometry('800x800')

        # Фрейм для полей ввода логина/пароля и кнопки "Войти"
        self.frame_fields = ttk.Frame(self)
        self.frame_fields.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.login_title = ttk.Label(self.frame_fields, text='Логин')
        self.login_title.pack(anchor='center')

        self.login_entry = ttk.Entry(self.frame_fields, width=30)
        self.login_entry.pack(anchor='center')

        self.password_title = ttk.Label(self.frame_fields, text='Пароль')
        self.password_title.pack(anchor='center')

        self.password_entry = ttk.Entry(self.frame_fields, width=30, show='*')
        self.password_entry.pack(anchor='center')

        self.login_button = ttk.Button(self.frame_fields, text='Войти', command=self.login)
        self.login_button.pack(anchor='center', pady=10)

        # Метка для вывода сообщения о результате авторизации
        self.login_message = ttk.Label(self.frame_fields, text='')
        self.login_message.pack(anchor='center', pady=10)

        # Фрейм для капчи (пока пустой, будет реализован позже)
        self.frame_captcha = ttk.Frame(self)
        self.frame_captcha.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def login(self):
        """
        Обрабатывает нажатие кнопки "Войти".

        Получает логин и пароль из полей ввода, вызывает метод
        ``UserController.auth()`` для аутентификации. При успешном входе
        пользователя с ролью 'admin' открывает панель администратора.
        """
        from Demo.Views.AdminView import AdminView
        login = self.login_entry.get()
        password = self.password_entry.get()

        user = UserController.auth(login, password)
        self.login_message['text'] = user['message']

        if user['success']:
            if user['user'].role == 'admin':
                window = AdminView()
                self.destroy()


if __name__ == '__main__':
    window = AuthView()
    window.mainloop()
