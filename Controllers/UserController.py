'''
класс для реализации методов CRUD
'''
from Models.User import *
from bcrypt import *
class UserController:
    '''
    в классе реализованы методы CRUD для класса User
    registration - создание нового пользователя
    auth - авторизация пользователя
    get - получение пользователей
    blocked - блокировка пользователя
    update - обновление пользователя
    delete - удаление пользователя
    check_password - проверка пароля ?
    check_date_auth - проверка даты авторизации
    '''
    @staticmethod
    def registration(login: str, password: str, role = 'user') -> dict:
        '''
        создание нового пользователя
        :param login:
        :param password: -> пароль зашифроввать
        :return: словарь в виде json {success: bool, message: str, user: User}
        '''
        # try:
        #     pass
        # except Exception as e:
        #     return {'success': False, 'message': e, 'user': None}
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
        '''
        авторизация пользователя
        :param login:
        :param password: должен быть проверен на хэш
        :return:
            словарь в виде json {'success': bool, 'message': str, 'user': User}
        '''
        try:
            user = User.get_or_none(login=login)
            if user is None:
                return {'success': False, 'message': f'Вы ввели неверный логин или пароль./n Пожалуйста проверьте ещё раз введенные данные', 'user': None}

            if checkpw(password.encode('utf -8'), user.password.encode('utf -8')) == False:
                return {'success': False, 'message': f'Вы ввели неверный логин или пароль./n Пожалуйста проверьте ещё раз введенные данные', 'user': None}
            return {'success': True, 'message': 'Вы успешно авторизовались', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def get():
        '''
        получение всех пользователей из таблицы Базы данных
        :return:
            список объектов таблицы user (пользователей)
        '''
        try:
            users = User.select()
            return {'success': True, 'message': 'Вывод пользователей', 'users': users}

        except Exception as e:
            return  {'success': False, 'message': e, 'user': None}
    @staticmethod
    def blocked(id: int):
        '''
        блокировка пользователя
        :param id:
        :return:
            словарь в виде json {'success': bool, 'message': str, 'user': User}
        '''
        pass
    @staticmethod
    def update(id: int, **filds: dict) -> dict:
        '''
        обновление пользователя
        :param id: идентификатор пользователя
        :param filds: ввод название поля и его новое значение login = new_login, password = new_password
        :return:
            словарь в виде json {'success': bool, 'message': str, 'user': User}
        '''
        try:
            # user = User.get_or_none(id=id)
            # if user is None:
            #     return {'success': False, 'message': 'Пользователь не найден', 'user': None}
            for key, value in filds.items():
                if key == 'password':
                    value = hashpw(value.encode(), gensalt())
                User.update({key: value}).where(User.id == id).execute()
            return {'success': True, 'message': 'Пользователь обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def new_update(id: int, login=None,password=None,blocked = None, role=None) -> dict:
        try:
            dict = {}
            if login:
                dict['login'] = login
            if password:
                dict['password'] = hashpw(password.encode(), gensalt())
            if blocked:
                dict['blocked'] = blocked
            if role:
                dict['role'] = role
            User.update(dict).where(User.id == id).execute()
            return {'success': True, 'message': 'Пользователь обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}
    @staticmethod
    def update_password(id: int, password: str) -> dict:
        '''
        обновление пароля пользователя
        :param id:
        :param password:
        :return:
            словарь в виде json {'success': bool, 'message': str, 'user': User}
        '''
        try:
            User.update({'password': hashpw(password.encode(), gensalt())}).where(User.id == id).execute()
            return {'success': True, 'message': 'Пароль обновлен', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}

    @staticmethod
    def delete(id: int):
        '''
        удаление пользователя
        :param id:
        :return:
            словарь в виде json {'success': bool, 'message': str, 'user': User}
        '''
        try:
            User.delete().where(User.id == id).execute()
            return {'success': True, 'message': 'Пользователь удален', 'user': None}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}



if __name__ == '__main__':
    print("Тест создания пользователя")
    print(UserController().registration('admin', 'admin', 'admin'))
    print("Тест авторизации")
    print(UserController.auth('admin', 'admin')) # не работает
    print("Тест получения пользователей")
    for user in UserController.get()['users']:
        print(user.login,user.role,user.bloked)
    print("Тест обновления пользователя")
    print(UserController.update(1, login='user', password='user', role='admin', bloked=True))
    print("Тест снова обновления пользователя")
    print(UserController.new_update(1))