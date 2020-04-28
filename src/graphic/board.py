from tkinter import *
from tkinter import ttk
from core.algogen_core import Game
from time import sleep
import core.algogen_core as core
import math
import graphic.options as o

BOARD_SIZE = 400
BORDER_SIZE = 5
PHASE_PLACEMENT = 0
PHASE_TIR_ALLIE = 1
PHASE_TIR_ENNEMI = 2
FONT_BORDER = 7


# Classe héritant de la classe Frame de tkinter
class Board(ttk.Frame):
    """
    Classe héritant de la classe Frame TKinter utilisé pour la création
    du plateau de jeu contre une intelligence artificielle.

    Attributs
    ---------
    self : base_app
       référence vers le singleton App : la fenêtre principale
    cells_by_line
        nombre de cellules par ligne, il est égal au nombre de cellules
        par colonnes
    game
        référence vers une instance de la classe Game, elle correspond
        au modèle d'une partie de bataille navale
    base_app
        référence vers le singleton App
    human
        booléen indiquant si un humain joue sur la grille de gauche

    Methodes
    --------
    draw()
        affiche le menu de jeu
    draw_grid(canvas, name)
        construit une grille dans le canvas indiqué en parametre, on
        indique le nom du canvas pour paramètrer les appels callback
    boardleft_callback(event)
        fonction callback du canvas du joueur de gauche, elle interprete
        le click émis puis envoie au modèle Game l'action a effectué
    boardright_callback(event)
        fonction callback du canvas du joueur de droite, elle interprete
        le click émis puis envoie au modèle Game l'action a effectué
    back()
        supprime les items de la fenêtre puis appel la fonction
        d'affichage du menu principal
    clear()
        nettoie les items présentes dans la fenêtre
    ready_clicked()
        évenement déclenché grâce au bouton Prêt, on commence dans la
        partie quand ce bouton est cliquer
    render_board(canvas, board, ennemy)
        affiche le rendu d'un board, cette fonction est appelé après
        une action effectué dans le modèle. On assigne le canvas sur
        lequel dessiner puis le contenu du board est donné via un
        tableau à deux dimensions nommé board, on ajoute à ça un
        booléen ennemy qui indique si le board est un board ennemi,
        ce qui implique que l'on doit cacher certaines informations
    paint_cell(canvas, coords, color)
        dessine un rectangle de couleur 'color' a la coordonée 'coords'
        dans le canvas entré en paramètre
    cell_coords(x, y)
        fonction outils qui transforme des coordonnées brut de canvas
        en coordonée grille (ex : 3,4;4,6 -> 3;5)
    draw_grid_coords(canvas)
        affiche les coordonnées sur les deux grilles
    game_won(winner)
        déclare un joueur du nom de 'winner' gagnant de la partie, la
        partie s'arrête
    ask_ia()
        récupère le prochain coup jouer par l'IA désigné par le modèle
        retourne 1 en cas de victoire
    """
    def __init__(self, base_app, human=True):
        super().__init__(base_app.master)
        self.cells_by_line = o.options_grid_size
        self.game = Game()
        self.base_app = base_app
        self.human = human
        root = base_app.master

        # Attributs graphiques et placements
        self.button_back = ttk.Button(
            root,
            text="Retour",
            command=self.back
        )
        if human:
            grid_name = "Ma grille"
        else:
            grid_name = "Joueur 1"
        self.board_left_name = Label(
            root,
            text=grid_name,
            font=("Helvetica", 16)
        )
        if human:
            grid_name = "Grille adverse"
        else:
            grid_name = "Joueur 2"
        self.board_right_name = Label(
            root,
            text=grid_name,
            font=("Helvetica", 16)
        )
        self.board_left = Canvas(
            root,
            width=BOARD_SIZE + 2 * BORDER_SIZE,
            height=BOARD_SIZE + 2 * BORDER_SIZE
        )
        self.board_right = Canvas(
            root,
            width=BOARD_SIZE + 2 * BORDER_SIZE,
            height=BOARD_SIZE + 2 * BORDER_SIZE
        )
        self.red_label = Label(
            root,
            text="Case rouge : Bateau touché",
            fg="red"
        )
        self.brown_label = Label(
            root,
            text="Case marron : Bateau coulé",
            fg="brown"
        )
        self.yellow_label = Label(
            root,
            text="Case bleue : Tir manqué",
            fg="blue"
        )
        self.grey_label = Label(
            root,
            text="Case grise : Pièce de bateau"
        )
        self.button_ready = ttk.Button(
            root,
            text="Prêt",
            command=self.ready_clicked
        )
        if human:
            label_text = "Phase de jeu : Placez vos bateaux."
        else:
            label_text = ""
        self.phase_label = Label(
            root,
            text=label_text
        )
        if human:
            self.boat_size_name = Label(
                root,
                text="Taille bateau"
            )
            self.boat_size = IntVar()
            self.boat_size.set(3)
            self.boat_size_entry = Entry(
                root,
                textvariable=self.boat_size,
                width=1
            )
            self.orientation_name = Label(
                root,
                text="Orientation"
            )
            self.orientation = StringVar()
            self.orientation_choices = {
                "Nord",
                "Nord",
                "Ouest",
                "Est",
                "Sud"
            }
            self.orientation.set("Nord")
            self.orientation_menu = ttk.OptionMenu(
                root,
                self.orientation,
                *self.orientation_choices
            )

    # Place les éléments graphiques dans la fenêtre
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
        self.button_ready.grid(row=3, column=3)
        self.phase_label.grid(row=3, column=0, sticky=W)
        if self.human:
            self.boat_size_name.grid(row=3, column=1, sticky=W)
            self.boat_size_entry.grid(row=3, column=1)
            self.orientation_name.grid(row=3, column=2, sticky=W)
            self.orientation_menu.grid(row=3, column=2, sticky=E)

        self.draw_grid(self.board_left, "left")
        self.draw_grid(self.board_right, "right")
        if not self.human:
            self.game.place_random(
                "all",
                o.options_ship_number,
                min(o.options_min_boat_size, o.options_grid_size),
                min(o.options_max_boat_size, o.options_grid_size))
            self.render_board(
                self.board_right,
                self.game.get_display_board("right"),
                ennemy=False)
        else:
            self.game.place_random(
                "right",
                o.options_ship_number,
                min(o.options_min_boat_size, o.options_grid_size),
                min(o.options_max_boat_size, o.options_grid_size))
        self.render_board(
            self.board_left,
            self.game.get_display_board("left"),
            ennemy=False)

    def draw_grid(self, canvas, name):
        canvas.create_rectangle(
            BORDER_SIZE,
            BORDER_SIZE,
            BOARD_SIZE + BORDER_SIZE,
            BOARD_SIZE + BORDER_SIZE
        )
        cell_size = BOARD_SIZE / self.cells_by_line
        # Tracé des lignes
        for i in range(1, self.cells_by_line):
            canvas.create_line(
                i * cell_size + BORDER_SIZE,
                BORDER_SIZE,
                i * cell_size + BORDER_SIZE,
                BORDER_SIZE + BOARD_SIZE
            )
        for i in range(1, self.cells_by_line):
            canvas.create_line(
                BORDER_SIZE,
                i * cell_size + BORDER_SIZE,
                BORDER_SIZE + BOARD_SIZE,
                i * cell_size + BORDER_SIZE
            )
        # Mapping des cellules
        if name == "left" and self.human:
            canvas.bind("<Button-1>", self.boardleft_callback)
        elif self.human:
            canvas.bind("<Button-1>", self.boardright_callback)
        self.draw_grid_coords(canvas)

    def boardleft_callback(self, event):
        if self.game.game_state == core.BOATS_PLACEMENT:
            res = self.game.place_boat(
                "left",
                self.cell_coords(event.x, event.y),
                self.boat_size.get(),
                self.orientation.get()
            )
            if res is not False:
                self.render_board(
                    self.board_left,
                    self.game.get_display_board("left")
                )

    def boardright_callback(self, event):
        if self.game.game_state == core.ATTACK:
            res = self.game.attack(
                "right",
                self.cell_coords(event.x, event.y)
            )
            self.game.get_display_board("right")
            self.render_board(
                self.board_right,
                self.game.get_display_board("right"),
                ennemy=True
            )
            if res == core.NO_ACTION:
                # Case déja cliqué avant
                return
            if res == core.WIN_ACTION:
                self.game_won("gauche")
            else:
                self.ask_ia()
                self.render_board(
                    self.board_left,
                    self.game.get_display_board("left"),
                    ennemy=False
                )

    def back(self):
        self.clear()
        self.base_app.home_draw()

    def clear(self):
        for widget in self.base_app.master.winfo_children():
            widget.destroy()

    def ready_clicked(self):
        if self.human:
            if self.game.game_begin():
                self.button_ready.destroy()
                self.orientation_name.destroy()
                self.orientation_menu.destroy()
                self.boat_size_name.destroy()
                self.boat_size_entry.destroy()
                self.phase_label.configure(
                    text="Phase de jeu : Tirez sur la grille ennemi."
                )
        else:
            self.button_ready.destroy()
            while 1:
                won = self.ask_ia(0, "left")
                self.render_board(
                    self.board_left,
                    self.game.get_display_board("left"),
                    ennemy=False
                )
                if won == 1:
                    break
                self.board_left.update()
                sleep(1)
                self.board_left.update_idletasks()
                won = self.ask_ia(1, "right")
                self.render_board(
                    self.board_right,
                    self.game.get_display_board("right"),
                    ennemy=False
                )
                if won == 1:
                    break
                self.board_right.update()
                sleep(1)

    def render_board(self, canvas, board, ennemy=False):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == core.EMPTY_CELL:
                    color = "white"
                elif board[i][j] == core.BOAT_CELL:
                    if ennemy is True:
                        color = "white"
                    else:
                        color = "grey"
                elif board[i][j] == core.HIT_CELL:
                    color = "red"
                elif board[i][j] == core.DROWN_CELL:
                    color = "brown"
                else:
                    color = "blue"
                self.paint_cell(canvas, [i, j], color)

    def paint_cell(self, canvas, coords, color):
        if min(coords) < 0 or max(coords) > self.cells_by_line - 1:
            return
        cell_size = BOARD_SIZE / self.cells_by_line
        canvas.create_rectangle(
            BORDER_SIZE + (coords[0]) * cell_size,
            BORDER_SIZE + (coords[1]) * cell_size,
            BORDER_SIZE + (coords[0] + 1) * cell_size,
            BORDER_SIZE + (coords[1] + 1) * cell_size,
            fill=color
        )
        self.draw_grid_coords(canvas)

    def cell_coords(self, x, y):
        return [math.floor((x - BORDER_SIZE) * self.cells_by_line
                           / BOARD_SIZE),
                math.floor((y - BORDER_SIZE) * self.cells_by_line
                           / BOARD_SIZE)
                ]

    def draw_grid_coords(self, canvas):
        cell_size = BOARD_SIZE / self.cells_by_line
        x_coord = "A"
        y_coord = "0"
        canvas.delete("coord")
        canvas.create_text(
            BORDER_SIZE + FONT_BORDER * 2,
            BORDER_SIZE + FONT_BORDER,
            font=("Helvetica", 12),
            text=x_coord + " / " + y_coord,
            tags="coord")
        # Tracé des lignes
        for i in range(1, self.cells_by_line):
            x_coord = chr(ord(x_coord) + 1)
            canvas.create_text(
                i * cell_size + BORDER_SIZE + FONT_BORDER,
                BORDER_SIZE + FONT_BORDER,
                font=("Helvetica", 12),
                text=x_coord,
                tags="coord")
        for i in range(1, self.cells_by_line):
            y_coord = chr(ord(y_coord) + 1)
            canvas.create_text(
                BORDER_SIZE + FONT_BORDER,
                i * cell_size + BORDER_SIZE + FONT_BORDER,
                font=("Helvetica", 12),
                text=y_coord,
                tags="coord")

    def game_won(self, winner):
        self.board_left.unbind("<Button 1>")
        self.board_right.unbind("<Button 1>")
        if winner == "right" and self.human:
            winner = "IA génétique"
        elif self.human:
            winner = "humain"
        elif winner == "right":
            winner = "2"
        else:
            winner = "1"
        self.phase_label.configure(text="Gagnant : Joueur " + winner)

    def ask_ia(self, index=0, to_attack="left"):
        if self.base_app.get_model().play(
                self.game,
                ia_index=index,
                to_attack=to_attack):
            if index == 0:
                self.game_won("right")
            else:
                self.game_won("left")
            return 1
        return 0
