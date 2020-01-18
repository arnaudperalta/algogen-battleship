from tkinter import ttk
from options import Options
from home import *


class App(ttk.Frame):
    def __init__(self, model):
        super().__init__(None)
        self.pack()

    def build(self):
        root = self.master
        root.title('AlgoGen Battleship')
        root.geometry("400x400")
        root.resizable(0, 0)
        self.home_draw()

    def home_draw(self):
        self.clear_frame()
        home_build(self.master)

    def quit_app(self):
        self.master.quit

    def options_draw(self):
        self.clear_frame()
        options = Options(self.master)
        options.build()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

