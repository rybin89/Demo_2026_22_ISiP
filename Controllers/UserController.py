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
    def registration(login: str, password: str) -> dict:
        '''
        создание нового пользователя
        :param login:
        :param password: -> пароль зашифроввать
        :return: словарь в виде json {success: bool, message: str, user: User}
        '''
        try:
            user = User.get_or_none(login=login)
            if user:
                return {'success': False, 'message': 'Такой логин уже занят', 'user': None}
            hash_password = hashpw(password.encode(), gensalt())
            user = User.create(login=login, password=hash_password)
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
            print(user.password)
            if checkpw(password.encode('utf -8'), user.password.encode('utf -8')) == False:
                return {'success': False, 'message': f'Вы ввели неверный логин или пароль./n Пожалуйста проверьте ещё раз введенные данные', 'user': None}
            return {'success': True, 'message': 'Вы успешно авторизовались', 'user': user}
        except Exception as e:
            return {'success': False, 'message': e, 'user': None}


if __name__ == '__main__':
    print("Тест создания пользователя")
    print(UserController().registration('test1', 'test'))
    print("Тест авторизации")
    print(UserController.auth('test1', 'test')) # не работает