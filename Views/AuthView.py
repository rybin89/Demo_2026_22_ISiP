'''
Создание окна авторизации
'''
from tkinter import *
from tkinter import ttk

from Controllers.UserController import UserController
from Views.AdminView import AdminView

class AuthView(Tk):
    '''
    Создание окна авторизации
        self - объект класса AuthView
        название - название окна 'Авторизация'
        текстовые поля 'логин', 'пароль' и кнопку "Войти".
        Поля "Логин" и "Пароль" должны быть обязательными для заполнения.
        При неверно введенных данных, пользователь должен получить сообщение об ошибке
        "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные".
        Фрейм с графической Капчей


    '''
    def __init__(self):
        super().__init__() # Инициализация родительского класса Tk - методы и классы, которые были определены в родительском классе

        # Свойства данного окна
        # Название окна
        self.title('Авторизация')
        self.geometry('800x800') # Размеры окна
        # Фрейм для полей 'логин', 'пароль' и кнопки "Войти".
        self.frame_filds = ttk.Frame(self)
        self.frame_filds.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.login_title = ttk.Label(self.frame_filds, text='Логин')
        self.login_title.pack(anchor='center')

        self.login_entry = ttk.Entry(self.frame_filds, width=30)
        self.login_entry.pack(anchor='center')

        self.password_title = ttk.Label(self.frame_filds, text='Пароль')
        self.password_title.pack(anchor='center')

        self.password_entry = ttk.Entry(self.frame_filds, width=30, show='*')
        self.password_entry.pack(anchor='center')

        self.login_button = ttk.Button(self.frame_filds, text='Войти', command=self.login)
        self.login_button.pack(anchor='center', pady=10)
        # Сообщение об выполнении авторизации
        self.login_message = ttk.Label(self.frame_filds, text='')
        self.login_message.pack(anchor='center', pady=10)

        self.frame_captcha = ttk.Frame(self)
        self.frame_captcha.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ## Captcha ###
    def login(self):
        login = self.login_entry.get() # Получение строки логина из поля ввода Логин
        password = self.password_entry.get() # Получение строки логина из поля ввода Пароль

        # Вызов функции авторизации из класса UserController
        user = UserController.auth(login, password)
        self.login_message['text'] = user['message']
        ## если пользователь администратор то открываем окно AdminView
        if user['success']:
            if user['user'].role == 'admin':
                window = AdminView()
                self.destroy()

if __name__ == '__main__':
    window = AuthView()
    window.mainloop()