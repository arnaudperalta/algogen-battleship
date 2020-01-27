from tkinter import *
from tkinter import ttk
from algogen_core import Core

# Classe héritant de la classe Frame de tkinter

# TODO quand on quitte le trainer il faut nettoyer tout le model car les options peuvent se faire modifier


class Trainer(ttk.Frame):
    def __init__(self, base_app, model):
        super().__init__(base_app.master)
        self.model = model
        self.base_app = base_app
        root = base_app.master

        self.results = Text(self.master, width=100, height=30)
        self.fulltrain_button = ttk.Button(root, text="Entrainement complet")
        self.steptrain_button = ttk.Button(root, text="Entrainement pas à pas")
        self.back_button = ttk.Button(root, text="Retour", command=self.back)

    def draw(self):
        self.results.pack(side=TOP)
        self.fulltrain_button.pack(side=RIGHT, padx=30)
        self.steptrain_button.pack(side=RIGHT, padx=120)
        self.back_button.pack(side=LEFT, padx=30)

    def back(self):
        self.clear()
        self.base_app.home_draw()

    def clear(self):
        for widget in self.base_app.master.winfo_children():
            widget.destroy()

    def fulltrain(self):
        while self.model.train():
            print(self.model.pop_info())

    def steptrain(self):
        if self.model.train():
            print(self.model.pop_info())

