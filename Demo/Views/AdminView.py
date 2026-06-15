"""
Модуль панели администратора.

Предоставляет графический интерфейс для управления пользователями:
создание новых пользователей, просмотр списка всех пользователей
в виде таблицы и редактирование существующих записей.

Пример:
    >>> from Views.AdminView import AdminView
    >>> window = AdminView()
    >>> window.mainloop()
"""
from tkinter import *
from tkinter import ttk

from Demo.Controllers.UserController import UserController


class AdminView(Tk):
    """
    Панель администратора системы.

    Предоставляет функционал для:
    - добавления новых пользователей;
    - просмотра списка всех пользователей в виде таблицы;
    - перехода к окну редактирования выбранного пользователя.

    Attributes:
        title (str): Заголовок окна — 'Панель администратора'.
        geometry (str): Размер окна — 800x800 пикселей.
        login_entry (Entry): Поле ввода логина нового пользователя.
        password_entry (Entry): Поле ввода пароля нового пользователя.
        roles_var (StringVar): Переменная для выбора роли из выпадающего списка.
    """
    def __init__(self):
        """Инициализирует окно панели администратора и все его элементы."""
        super().__init__()
        self.title("Панель администратора")
        self.geometry("800x800")

        # === Фрейм для создания нового пользователя ===
        self.new_user_frame = ttk.Frame(self)
        self.new_user_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.add_label = ttk.Label(self.new_user_frame, text='Добавить нового пользователя')
        self.add_label.pack(anchor='center', pady=10)

        self.login_title = ttk.Label(self.new_user_frame, text='Введите Логин')
        self.login_title.pack(anchor='center')

        self.login_entry = ttk.Entry(self.new_user_frame, width=30)
        self.login_entry.pack(anchor='center')

        self.password_title = ttk.Label(self.new_user_frame, text='Введите Пароль')
        self.password_title.pack(anchor='center')

        self.password_entry = ttk.Entry(self.new_user_frame, width=30, show='*')
        self.password_entry.pack(anchor='center')

        # Выпадающий список для выбора роли
        self.roles = ["Пользователь", "Администратор"]
        self.roles_var = StringVar(self.new_user_frame, value=self.roles[0])

        self.label = ttk.Label(self.new_user_frame, textvariable=self.roles_var)
        self.label.pack(anchor='center', padx=6, pady=6)

        self.combobox = ttk.Combobox(self.new_user_frame, textvariable=self.roles_var, values=self.roles)
        self.combobox.pack(anchor='center', padx=6, pady=6)

        self.login_button = ttk.Button(self.new_user_frame, text='Зарегистрировать', command=self.login)
        self.login_button.pack(anchor='center', pady=10)

        # Метка для сообщения о результате регистрации
        self.login_message = ttk.Label(self.new_user_frame, text='')
        self.login_message.pack(anchor='center', pady=10)

        # === Фрейм для таблицы пользователей ===
        self.users_frame = ttk.Frame(self)
        self.users_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.columns = ('login', 'role', 'blocked')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        self.table()
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def item_selected(self, event):
        """
        Обрабатывает выбор строки в таблице пользователей.

        При двойном клике или выборе пользователя из таблицы
        открывает окно редактирования EditUser и закрывает текущее окно.

        Args:
            event: Событие выбора элемента в Treeview.
        """
        from Demo.Views.EditUser import EditUser
        self.item = self.tree.selection()[0]
        self.user_data = self.tree.item(self.item)['values'][0]
        window = EditUser(self.user_data)
        self.destroy()

    def table(self):
        """
        Заполняет таблицу данными всех пользователей.

        Очищает таблицу, получает список пользователей из контроллера,
        преобразует значения полей ``bloked`` и ``role`` в читаемый текст
        и отображает их в таблице.
        """
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = UserController.get()['users']
        rows = []

        for user in users:
            # Преобразование поля blocked в читаемый текст
            user.bloked = 'Да' if user.bloked else 'Нет'
            # Преобразование роли в русское название
            user.role = 'Пользователь' if user.role == 'user' else 'Администратор'

            rows.append((user.login, user.role, user.bloked))

        # Заголовки таблицы
        self.tree.heading('login', text='Логин')
        self.tree.heading('role', text='Роль')
        self.tree.heading('blocked', text='Заблокирован')

        # Заполнение таблицы строками
        for item in rows:
            self.tree.insert('', END, values=item)

    def login(self):
        """
        Регистрирует нового пользователя из данных формы.

        Получает логин, пароль и роль из полей ввода, проверяет
        заполнение обязательных полей и вызывает метод
        ``UserController.registration()`` для создания пользователя.
        После регистрации обновляет таблицу.
        """
        login = self.login_entry.get()
        password = self.password_entry.get()
        role = self.roles_var.get()

        role = 'user' if role == 'Пользователь' else 'admin'

        if login == '' or password == '':
            self.login_message['text'] = 'Заполните все поля'
        else:
            user = UserController.registration(login, password, role)
            self.login_message['text'] = user['message']

        self.table()


if __name__ == "__main__":
    window = AdminView()
    window.mainloop()
