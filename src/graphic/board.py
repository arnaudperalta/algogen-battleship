from tkinter import *
from tkinter import ttk
import math

BOARD_SIZE = 400
BORDER_SIZE = 5
CELLS_BY_LINE = 5
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
        self.board_left = Canvas(frame_left.master
                                 , width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.board_left.pack(side=LEFT)
        self.board_right = Canvas(frame_right.master
                                  , width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.board_right.pack(side=RIGHT)

    def draw(self):
        self.draw_grid(self.board_left, "left")
        self.draw_grid(self.board_right, "right")

    def draw_grid(self, canvas, name):
        canvas.create_rectangle(BORDER_SIZE, BORDER_SIZE, BOARD_SIZE + BORDER_SIZE, BOARD_SIZE + BORDER_SIZE)
        cell_size = BOARD_SIZE / CELLS_BY_LINE
        # Tracé des lignes
        for i in range(1, CELLS_BY_LINE):
            canvas.create_line(i * cell_size + BORDER_SIZE, BORDER_SIZE
                               , i * cell_size + BORDER_SIZE, BORDER_SIZE + BOARD_SIZE)
        for i in range(1, CELLS_BY_LINE):
            canvas.create_line(BORDER_SIZE, i * cell_size + BORDER_SIZE
                               , BORDER_SIZE + BOARD_SIZE, i * cell_size + BORDER_SIZE)
        # Mapping des cellules
        for i in range(1, CELLS_BY_LINE):
            for j in range(1, CELLS_BY_LINE):
                if name == "left":
                    canvas.bind("<Button-1>", self.boardleft_callback)
                else:
                    canvas.bind("<Button-1>", self.boardright_callback)

    def boardleft_callback(self, event):
        self.paint_cell(self.board_left, cell_coords(event.x, event.y))

    def boardright_callback(self, event):
        self.paint_cell(self.board_right, cell_coords(event.x, event.y))


def paint_cell(self, canvas, coords):
    cell_size = BOARD_SIZE / CELLS_BY_LINE
    canvas.create_rectangle(BORDER_SIZE + (coords[0]) * cell_size
                            , BORDER_SIZE + (coords[1]) * cell_size
                            , BORDER_SIZE + (coords[0] + 1) * cell_size
                            , BORDER_SIZE + (coords[1] + 1) * cell_size
                            , fill="red")


# Transforme des coordonnées canvas en couple x,y de coords cellules
def cell_coords(x, y):
    return [math.floor((x - BORDER_SIZE) * CELLS_BY_LINE / BOARD_SIZE),
            math.floor((y - BORDER_SIZE) * CELLS_BY_LINE / BOARD_SIZE)]
