from tkinter import *
from tkinter import ttk
import math

BOARD_SIZE = 400
BORDER_SIZE = 5
CELLS_BY_LINE = 5
# Classe héritant de la classe Frame de tkinter


class Board(ttk.Frame):
    def __init__(self, base_app):
        super().__init__(base_app.master)
        self.base_app = base_app
        root = base_app.master

        # Attributs graphiques
        button_back = ttk.Button(root, text="Retour", command=self.back)
        button_back.grid(row=0, column=0, sticky=W)
        board_left_letters = Label(root, text="Ma grille", font=("Helvetica", 16))
        board_left_letters.grid(row=0, column=0)
        board_left_letters = Label(root, text="Grille adverse", font=("Helvetica", 16))
        board_left_letters.grid(row=0, column=1)
        self.board_left = Canvas(root, width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.board_left.grid(row=1, column=0)
        self.board_right = Canvas(root, width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.board_right.grid(row=1, column=1)

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
        paint_cell(self.board_left, cell_coords(event.x, event.y))

    def boardright_callback(self, event):
        paint_cell(self.board_right, cell_coords(event.x, event.y))

    def back(self):
        self.base_app.home_draw()


def paint_cell(canvas, coords):
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
