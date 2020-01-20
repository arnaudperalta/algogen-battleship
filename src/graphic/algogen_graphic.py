from tkinter import ttk
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
        train_button = ttk.Button(root, text='Entraîner IA Génétique', command=root.quit)
        train_button.pack()
        play_button = ttk.Button(root, text='Jouer vs IA Génétique', command=self.play_vs_ia)
        play_button.pack()
        ia_button = ttk.Button(root, text='IA vs IA', command=root.quit)
        ia_button.pack()
        options_button = ttk.Button(root, text='Options', command=self.options_draw)
        options_button.pack()
        quit_button = ttk.Button(root, text='Quitter', command=root.destroy)
        quit_button.pack()

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
