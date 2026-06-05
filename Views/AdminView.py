'''
Панель администратора системы
'''
from tkinter import *
from tkinter import ttk

from Controllers.UserController import UserController
from Views.EditUser import *


class AdminView(Tk):
    '''
    Панель администратора системы
    функционал для добавления новых пользователей,
    изменения данных  текущих пользователей
    снятие  блокировки
    Вывод всех пользователей в виде таблицы
     '''
    def __init__(self):
        super().__init__()
        self.title("Панель администратора")
        self.geometry("800x800")
        # Фрейм для вывода данных для создания нового пользователя
        self.new_user_frame = ttk.Frame(self)
        self.new_user_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        # Поля Логин, Пароль, Роль
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

        # Роль
        self.roles = ["Пользователь", "Администратор"]
        # по умолчанию будет выбран первый элемент из languages
        self.roles_var = StringVar(self.new_user_frame,value=self.roles[0])

        self.label = ttk.Label(self.new_user_frame,textvariable=self.roles_var)
        self.label.pack(anchor='center', padx=6, pady=6)

        self.combobox = ttk.Combobox(self.new_user_frame,textvariable=self.roles_var, values=self.roles)
        self.combobox.pack(anchor='center', padx=6, pady=6)

        self.login_button = ttk.Button(self.new_user_frame, text='Зарегистрировать', command=self.login)
        self.login_button.pack(anchor='center', pady=10)
        # Сообщение об выполнении авторизации
        self.login_message = ttk.Label(self.new_user_frame, text='')
        self.login_message.pack(anchor='center', pady=10)

        # Фрейм для вывода данных пользователей в виде таблицы
        self.users_frame = ttk.Frame(self)
        self.users_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        # Определяем столбцы таблицы
        self.columns= ('login', 'role', 'blocked')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        self.table()
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)



    #Таблица будет появлятся с помощью метода self.table()
    # метод item_selected() будет откудывать окно редактирования пользователя
    def item_selected(self, event):
        #атрибут item будет содержать строку
        self.item = self.tree.selection()[0]
        #атрибут user_data будет содержать значения из строки login
        self.user_data = self.tree.item(self.item)['values'][0]
        # Открыть окно редактирования пользователя
        window = EditUser(self.user_data)
        self.destroy()



    def table(self):
        # Очистка таблицы от данных
        for item in self.tree.get_children():
            self.tree.delete(item)
        # перменной users присваиваем словарь из метода get()
        users = UserController.get()['users']
        list = []
        for user in users:
            # У каждого пользователя изменить поле blocked на текст
            if user.bloked == True:
                user.bloked = 'Да'
            else:
                user.bloked = 'Нет'
            # У каждого пользователя изменить поле role на русское название
            if user.role == 'user':
                user.role = 'Пользователь'
            else:
                user.role = 'Администратор'

            list.append((user.login, user.role, user.bloked))
        # Заголовки таблицы
        self.tree.heading('login', text='Логин')
        self.tree.heading('role', text='Роль')
        self.tree.heading('blocked', text='Заблокирован')
        # Из списка list создаем строки таблицы
        for item in list:
            self.tree.insert('', END, values=item)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        roles = self.roles_var
        if roles == 'Пользователь':
            roles = 'user'
        else:
            roles = 'admin'
        if login == '' or password == '':
            self.login_message['text']='Заполните все поля'
        else:
            user = UserController.registration(login, password, roles)
            self.login_message['text'] = user['message']
        self.table()


if __name__ == "__main__":
    window = AdminView()
    window.mainloop()





