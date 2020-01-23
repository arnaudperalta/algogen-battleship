from tkinter import *
from tkinter import ttk
import math

BOARD_SIZE = 400
BORDER_SIZE = 5
CELLS_BY_LINE = 5
PHASE_PLACEMENT = 0
PHASE_TIR_ALLIE = 1
PHASE_TIR_ENNEMI = 2
FONT_BORDER = 7
# Classe héritant de la classe Frame de tkinter


class Board(ttk.Frame):
    def __init__(self, base_app):
        super().__init__(base_app.master)
        self.base_app = base_app
        root = base_app.master

        # Attributs graphiques et placements
        self.button_back = ttk.Button(root, text="Retour", command=self.back)
        self.board_left_name = Label(root, text="Ma grille", font=("Helvetica", 16))
        self.board_right_name = Label(root, text="Grille adverse", font=("Helvetica", 16))
        self.board_left = Canvas(root, width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.board_right = Canvas(root, width=BOARD_SIZE + 2 * BORDER_SIZE, height=BOARD_SIZE + 2 * BORDER_SIZE)
        self.red_label = Label(root, text="Case rouge : Bateau touché", fg="red")
        self.brown_label = Label(root, text="Case marron : Bateau coulé", fg="brown")
        self.yellow_label = Label(root, text="Case bleue : Tir manqué", fg="blue")
        self.grey_label = Label(root, text="Case grise : Pièce de bateau")
        self.button_ready = ttk.Button(root, text="Prêt", command=self.ready_clicked)
        self.phase_label = Label(root, text="Phase de jeu : Placez vos bateaux.")
        # On désigne une phase de jeu
        self.phase = PHASE_PLACEMENT

    def draw(self):
        self.button_back.grid(row=0, column=0, sticky=W)
        self.board_left_name.grid(row=0, column=1, sticky=W)
        self.board_right_name.grid(row=0, column=2)
        self.board_left.grid(row=1, column=0, columnspan=2)
        self.board_right.grid(row=1, column=2, columnspan=2)
        self.red_label.grid(row=2, column=0, sticky=W)
        self.brown_label.grid(row=2, column=1, sticky=W)
        self.yellow_label.grid(row=2, column=2)
        self.grey_label.grid(row=2, column=3)
        self.button_ready.grid(row=3, column=1)
        self.phase_label.grid(row=3, column=0, sticky=W)

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
        draw_grid_coords(canvas)

    def boardleft_callback(self, event):
        if self.phase == PHASE_PLACEMENT:
            # demande au model le resultat du tir puis paint la case selon la réponse
            paint_cell(self.board_left, cell_coords(event.x, event.y), "grey")

    def boardright_callback(self, event):
        if self.phase == PHASE_TIR_ALLIE:
            # demande au model le resultat du tir puis paint la case selon la réponse
            paint_cell(self.board_right, cell_coords(event.x, event.y), "blue")

    def back(self):
        self.clear()
        self.base_app.home_draw()

    def clear(self):
        for widget in self.base_app.master.winfo_children():
            widget.destroy()

    def ready_clicked(self):
        self.button_ready.destroy()
        self.phase = PHASE_TIR_ALLIE
        self.phase_label.configure(text="Phase de jeu : Tirez sur la grille ennemi.")


def paint_cell(canvas, coords, color):
    if min(coords) < 0 or max(coords) > CELLS_BY_LINE - 1:
        return
    cell_size = BOARD_SIZE / CELLS_BY_LINE
    canvas.create_rectangle(BORDER_SIZE + (coords[0]) * cell_size
                            , BORDER_SIZE + (coords[1]) * cell_size
                            , BORDER_SIZE + (coords[0] + 1) * cell_size
                            , BORDER_SIZE + (coords[1] + 1) * cell_size
                            , fill=color)
    draw_grid_coords(canvas)


# Transforme des coordonnées canvas en couple x,y de coords cellules
def cell_coords(x, y):
    return [math.floor((x - BORDER_SIZE) * CELLS_BY_LINE / BOARD_SIZE),
            math.floor((y - BORDER_SIZE) * CELLS_BY_LINE / BOARD_SIZE)]


def draw_grid_coords(canvas):
    cell_size = BOARD_SIZE / CELLS_BY_LINE
    x_coord = "A"
    y_coord = "0"
    canvas.delete("coord")
    canvas.create_text(BORDER_SIZE + FONT_BORDER * 2, BORDER_SIZE + FONT_BORDER, font=("Helvetica", 12)
                       , text=x_coord + " / " + y_coord, tags="coord")
    # Tracé des lignes
    for i in range(1, CELLS_BY_LINE):
        x_coord = chr(ord(x_coord) + 1)
        canvas.create_text(i * cell_size + BORDER_SIZE + FONT_BORDER, BORDER_SIZE + FONT_BORDER
                           , font=("Helvetica", 12), text=x_coord, tags="coord")
    for i in range(1, CELLS_BY_LINE):
        y_coord = chr(ord(y_coord) + 1)
        canvas.create_text(BORDER_SIZE + FONT_BORDER, i * cell_size + BORDER_SIZE + FONT_BORDER
                           , font=("Helvetica", 12), text=y_coord, tags="coord")
