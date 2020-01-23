from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from board import Board
from options import Options


class App(ttk.Frame):
    def __init__(self, model):
        super().__init__(None)
        self.pack()


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

        title = Label(text = "AlgoGen Battleship",font=("Helvetica",30))
        title.pack()
        #Frame contenant les 5 boutons princpaux du menu
        frame = Frame(root)
        play_button = ttk.Button(frame, text='Jouer vs IA Génétique', command=self.play_vs_ia, width = 20).pack()
        ia_button = ttk.Button(frame, text='IA vs IA', command=root.quit, width = 20).pack()
        train_button = ttk.Button(frame, text='Entraîner IA Génétique', command=root.quit, width = 20).pack()
        options_button = ttk.Button(frame, text='Options', command=self.options_draw, width = 20).pack(pady = 5)
        quit_button = ttk.Button(frame, text='Quitter', command=root.destroy, width = 20).pack(pady = 5)
        frame.pack(expand=YES)

        text_noms = Label(root,text="Arnaud Peralta, Yohann Goffart, Louis Pariente - Q1 2020",font=("Helvetica")).pack(side=BOTTOM)




    def play_vs_ia(self):
        self.clear_frame()
        board = Board(self)
        board.draw()

    def quit_app(self):
        self.master.quit

    def options_draw(self):
        self.clear_frame()
        options = Options(self.master, self)
        options.build()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def training_send(self, array):
        print("fonction appellé par le training")
