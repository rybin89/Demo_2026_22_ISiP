"""
Модуль окна редактирования пользователя.

Предоставляет графический интерфейс для изменения данных
конкретного пользователя: логина, пароля, роли и статуса блокировки.

Пример:
    >>> from Views.EditUser import EditUser
    >>> window = EditUser('admin')
    >>> window.mainloop()
"""
from tkinter import *
from tkinter import ttk

from Demo.Controllers.UserController import UserController


class EditUser(Tk):
    """
    Окно редактирования пользователя.

    Позволяет изменять логин, пароль, роль и статус блокировки
    выбранного пользователя. После сохранения изменений возвращает
    пользователя на панель администратора.

    Args:
        login: Логин редактируемого пользователя.

    Attributes:
        title (str): Заголовок окна, содержит логин пользователя.
        geometry (str): Размер окна — 800x800 пикселей.
        login_entry (Entry): Поле ввода нового логина.
        password_entry (Entry): Поле ввода нового пароля.
        roles_var (StringVar): Переменная выбора роли.
    """
    def __init__(self, login):
        """
        Инициализирует окно редактирования пользователя.

        Args:
            login: Логин пользователя, данные которого будут изменяться.
        """
        super().__init__()
        self.login = login
        self.title(f'Изменение пользователя {self.login}')
        self.geometry('800x800')

        # Фрейм для полей ввода
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

        # Выпадающий список для выбора роли
        self.roles = ["Пользователь", "Администратор"]
        self.roles_var = StringVar(self.frame_fields, value=self.roles[0])

        self.label = ttk.Label(self.frame_fields, textvariable=self.roles_var)
        self.label.pack(anchor='center', padx=6, pady=6)

        self.combobox = ttk.Combobox(self.frame_fields, textvariable=self.roles_var, values=self.roles)
        self.combobox.pack(anchor='center', padx=6, pady=6)

        self.blocked_button = ttk.Button(self.frame_fields, text='Блокировать', command=self.save)
        self.blocked_button.pack(anchor='center', pady=10)

        self.save_button = ttk.Button(self.frame_fields, text='Сохранить', command=self.save)
        self.save_button.pack(anchor='center', pady=10)

        # Метка для сообщения о результате сохранения
        self.login_message = ttk.Label(self.frame_fields, text='')
        self.login_message.pack(anchor='center', pady=10)

        # Фрейм для капчи (пока пустой)
        self.frame_captcha = ttk.Frame(self)
        self.frame_captcha.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def save(self):
        """
        Сохраняет изменения данных пользователя.

        Получает логин, пароль и роль из полей ввода и передаёт их
        в контроллер для обновления. После успешного сохранения
        открывает панель администратора.
        """
        login = self.login_entry.get()
        password = self.password_entry.get()
        role = self.roles_var.get()

        # Пока заглушка — требуется доработка логики сохранения
        # user = UserController.update(...)
        # self.login_message['text'] = user['message']
        pass


if __name__ == '__main__':
    from Demo.Views.AuthView import AuthView
    window = AuthView()
    window.mainloop()
