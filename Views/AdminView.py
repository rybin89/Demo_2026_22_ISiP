'''
Панель администратора системы
'''
from tkinter import *
from tkinter import ttk

from Controllers.UserController import *

class AdminView(Tk):
    def __init__(self):
        super().__init__()
        self.title("Панель администратора")
        self.geometry("800x800")
