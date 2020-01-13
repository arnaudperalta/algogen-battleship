from tkinter import *
# Fix pour bug visuel sur OSX
from tkinter import ttk
from home import Home


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

    def build(self):
        root = self.master
        root.title('AlgoGen Battleship')
        root.geometry("400x400")
        root.resizable(0, 0)
        home = Home(root)
        home.build()
