from tkinter import ttk
from tkinter import *
from algogen_chart import Chart
from board import Board
from trainer import Trainer
from options import Options


class App(ttk.Frame):
    def __init__(self, model):
        super().__init__(None)
        self.pack()
        self.model = model

    def get_model(self):
        return self.model

    def build(self):
        root = self.master
        root.title('AlgoGen Battleship')
        root.geometry("830x500")
        root.resizable(0, 0)
        self.home_draw()
        root.mainloop()

    def home_draw(self):
        self.clear_frame()
        root = self.master

        title = Label(text="AlgoGen Battleship", font=("Helvetica", 30))
        title.pack()
        # Frame contenant les 5 boutons princpaux du menu
        frame = Frame(root)
        ttk.Button(frame, text='Jouer vs IA Génétique', command=self.play_vs_ia, width=20).pack()
        ttk.Button(frame, text='IA vs IA', command=root.quit, width=20).pack()
        ttk.Button(frame, text='Entraîner IA Génétique', command=self.training_draw, width=20).pack()
        ttk.Button(frame, text='Statistiques', command=self.chart, width=20).pack()
        ttk.Button(frame, text='Options', command=self.options_draw, width=20).pack(pady=5)
        ttk.Button(frame, text='Quitter', command=root.destroy, width=20).pack(pady=5)
        frame.pack(expand=YES)

        Label(root, text="Arnaud Peralta, Yohann Goffart, Louis Pariente - Q1 2020",
                          font="Helvetica").pack(side=BOTTOM)

    def training_draw(self):
        self.clear_frame()
        trainer = Trainer(self, self.model)
        trainer.draw()

    def play_vs_ia(self):
        self.clear_frame()
        board = Board(self)
        board.draw()

    def quit_app(self):
        self.master.quit

    def chart(self):
        self.clear_frame()
        chart = Chart(self, self.model)
        chart.build()

    def options_draw(self):
        self.clear_frame()
        options = Options(self.master, self)
        options.build()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def training_send(self, array):
        print("fonction appellée par le training")

