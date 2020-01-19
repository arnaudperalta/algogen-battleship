from tkinter import *
from tkinter import ttk

# Classe héritant de la classe Frame de tkinter


class Board(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        # Attributs graphique
        frame_left = Frame(self.master)
        frame_left.pack(side=LEFT)
        frame_right = Frame(self.master)
        frame_right.pack(side=RIGHT)
        self.board_left = Canvas(frame_left.master, width=400, height=400)
        self.board_left.pack(side=LEFT)
        self.board_right = Canvas(frame_right.master, width=400, height=400)
        self.board_right.pack(side=RIGHT)

    def draw(self):
        draw_grid(self.board_left)
        draw_grid(self.board_right)


def draw_grid(canvas):
    canvas.create_rectangle(5, 5, 400, 400)
