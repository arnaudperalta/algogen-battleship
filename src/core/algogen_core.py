from genetic import Population
from genetic import Individu
from random import randint
import options as o
import genetic as g
from math import floor

# Etats des cellules
EMPTY_CELL = 0
BOAT_CELL = 1
HIT_CELL = 2
DROWN_CELL = 3
MISS_CELL = 4
# Action
NO_ACTION = 0
MISS_ACTION = 1
HIT_ACTION = 2
DROWN_ACTION = 3
WIN_ACTION = 4
# Phases de jeu
BOATS_PLACEMENT = 0
ATTACK = 1
PLAYER_LEFT_WIN = 2
PLAYER_RIGHT_WIN = 3


class Core:
    """
    Classe utilisé pour l'éxecution de l'algorithme génétique

    Attributs
    ---------
    pop
        Instance de la classe Population
    bot
        Individu désigné pour être l'IA qui jouera dans la section
        du programme Player vs IA

    Methodes
    --------
    train()
        Procède a l'éxecution de l'algorithme génétique sur la
        génération actuelle sur une génération. On y fait jouer une
        partie de bataille navale pour chaque pour chaque individu,
        on conserve les individus qui ont gagné la partie en un
        minimum de coup, on produit de nouveaux individus à partir des
        meilleurs (cross-over génétique) puis on mute toute la
        population.
    play()
        Simule une action joueur humain dans une partie, qui est une
        instance de Game.
    """
    def __init__(self):
        # Lecture des paramètres
        self.pop = Population(o.options_nbr_idv)
        self.bot = self.pop.get_idv(0)

    def train(self):
        # TODO call des fonctions plutot que d'édit direct les variables
        fit_tab = []
        fit_sum = 0
        for i in range(o.options_nbr_idv):
            self.bot = self.pop.idv_tab[i]
            self.bot.shoot_nb = 0
            game = Game()
            game.place_boat("right", [0, 0], 3, "Sud")
            game.place_boat("left", [0, 0], 3, "Sud")
            game.game_begin()
            ended = False
            while not ended:
                ended = self.play(game, "left")
            fit_tab.append((i, self.bot.fitness()))
            fit_sum += self.bot.fitness()
        fit_tab.sort(key=sort_second)
        saved = floor((o.options_saved_percentage / 100)
                      * o.options_nbr_idv)
        new_idv_tab = []
        for i in range(saved):
            (x, y) = fit_tab[i]
            new_idv_tab.append(self.pop.idv_tab[x])
        for i in range(o.options_nbr_idv - saved):
            idv1 = new_idv_tab[randint(0, saved - 1)]
            idv2 = new_idv_tab[randint(0, saved - 1)]
            new_idv_tab.append(g.merge(idv1, idv2))
        self.pop.idv_tab = new_idv_tab
        self.pop.mutate()
        self.pop.gen_fit_score.append(fit_sum/(len(self.pop.idv_tab)))
        self.pop.generation = self.pop.generation + 1
        return fit_tab

    # Return true si la partie est gagnée
    def play(self, game, to_attack="left"):
        coord = self.bot.play(game)
        if coord in game.get_free_cells("left"):
            res = game.attack(to_attack, coord)
            if res == HIT_ACTION:
                self.bot.notify = True
            if res == DROWN_ACTION:
                self.bot.notify_drown = True
            if res == WIN_ACTION:
                return True
            return False
        else:
            return self.play(game, to_attack)


def sort_second(val):
    return val[1]


class Game:
    """
    Classe utilisé pour l'éxecution de l'algorithme génétique

    Attributs
    ---------
    game_state
        Etat actuel de la partie:
            - phase de placement
            - phase d'attaque
            - partie remportée
    board1, board2
        Tableau a deux dimensions représentant une grille de jeu de
        bataille navale

    Methodes
    --------
    place_boat(board_name, coords, boat_size, orientation)
        place un bateau sur le board donné en paramètre, renvoie true
        si la place pour placer le bateau comme voulu a été suffisante
    attack(board_name, coords)
        simule une attaque sur le board donné en paramètre
        renvoie une action correspondante :
            - MISS_ACTION
            - DROWN_ACTION
            - WIN_ACTION
            - HIT_ACTION
    get_display_board(board)
        transforme un board du modèle Game en un board adapté à
        l'affichage et destiné au module graphic, ce board contient que
        des entiers de valeurs :
            - EMPTY_CELL
            - BOAT_CELL
            - HIT_CELL
            - DROWN_CELL
            - MISS_CELL
    game_begin()
        vérifie si un bateau est placé dans chaque grille puis démarre
        une partie de bataille navale
    game_reset()
        réinitialise l'instance de Game courante en ré-appelant le
        constructeur
    get_free_cells(board_name)
        retourne une liste de cases vide où l'IA pour
    """
    def __init__(self):
        self.game_state = BOATS_PLACEMENT
        self.board1 = create_board(o.options_grid_size)
        self.board2 = create_board(o.options_grid_size)

    def place_boat(self, board_name, coords, boat_size, orientation):
        if boat_size < 1:
            return False
        main_boat = Boat(boat_size)
        if board_name == "left":
            board = self.board1
        else:
            board = self.board2

        boat_coords = []
        if orientation == "Nord":
            for i in range(boat_size):
                if board[coords[0]][coords[1] - i] is not None \
                        or coords[1] - i < 0:
                    return False
                boat_coords.append([coords[0], coords[1] - i])
        elif orientation == "Ouest":
            for i in range(boat_size):
                if board[coords[0] - i][coords[1]] is not None \
                        or coords[0] - i < 0:
                    return False
                boat_coords.append([coords[0] - i, coords[1]])
        elif orientation == "Est":
            for i in range(boat_size):
                if board[coords[0] + i][coords[1]] is not None:
                    return False
                boat_coords.append([coords[0] + i, coords[1]])
        else:
            for i in range(boat_size):
                if board[coords[0]][coords[1] + i] is not None:
                    return False
                boat_coords.append([coords[0], coords[1] + i])

        board[boat_coords[0][0]][boat_coords[0][1]] = main_boat
        childs = main_boat.get_childs()
        for i in range(len(childs)):
            board[boat_coords[i + 1][0]][boat_coords[i + 1][1]] \
                = childs[i]
        return True

    def attack(self, board_name, coords):
        if board_name == "left":
            board = self.board1
        else:
            board = self.board2
        target = board[coords[0]][coords[1]]
        if target is None:
            board[coords[0]][coords[1]] = MISS_CELL
            return MISS_ACTION
        if not isinstance(target, Boat) or target.state != BOAT_CELL:
            return NO_ACTION
        if target.hit():
            for i in range(len(board)):
                for j in range(len(board)):
                    if isinstance(board[i][j], Boat) \
                            and board[i][j].state == BOAT_CELL:
                        return DROWN_ACTION
            return WIN_ACTION
        else:
            return HIT_ACTION

    def get_display_board(self, name):
        result = []
        if name == "left":
            board = self.board1
        else:
            board = self.board2
        for i in range(len(board)):
            line = []
            for j in range(len(board)):
                if board[i][j] is None:
                    line.append(EMPTY_CELL)
                elif board[i][j] == MISS_CELL:
                    line.append(MISS_CELL)
                else:
                    line.append(board[i][j].get_state())
            result.append(line)
        return result

    def game_begin(self):
        boat = False
        # Vérification du board 1
        for i in range(len(self.board1)):
            for j in range(len(self.board1)):
                if self.board1[i][j] is not None:
                    boat = True
                    break
            if boat:
                break
        if not boat:
            return False
        # Vérification du board 2
        boat = False
        for i in range(len(self.board2)):
            for j in range(len(self.board2)):
                if self.board2[i][j] is not None:
                    boat = True
                    break
            if boat:
                break
        if not boat:
            return False
        self.game_state = ATTACK
        return True

    def game_reset(self):
        self.__init__()

    def get_free_cells(self, board_name):
        cells = []
        if "left" == board_name:
            board = self.board1
        else:
            board = self.board2
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] is None or isinstance(board[i][j], Boat)\
                        and board[i][j].state == BOAT_CELL:
                    cells.append([i, j])
        return cells


class Boat:
    """
    Classe utilisé pour la simulation d'une case de bateau au sein d'une
    grille de bataille navale, le constructeur possède une récusrvité
    indirecte, un bateau sur une grille possède une instance de Boat
    'mère' (là ou le joueur a cliquer) puis créé des instances 'fils' de
    boat afin de construire le reste du bateau suivant la taille en
    parametre du constructeur

    Attributs
    ---------
    parent : parent
        référence vers l'instance Boat mère, si on se situe dans une
        instance fils
    size : size
        taille du bateau
    child
        liste des instances de Boat 'fils' qui ont comme parent 'self'
    state
        état de la case :
            - BOAT_CELL
            - HIT_CELL
            - DROWN_CELL

    Methodes
    --------
    ini_boat()
        initialise toutes les instances 'fils' de cette instance
    get_state()
        retourne l'état de la case representé par cette instance
    set_state()
        modifie l'état de la case representé par cette instance
    get_childs()
        retourne la liste des 'fils de cette instance
    hit()
        attaque la case representé par cette instance, si cette case
        n'était pas encore touchée, elle devient HIT_CELL, si tout ces
        enfants sont touchée et que cette instance est mère, dans ce cas
        on change tout les états des enfants et de cette instance en
        DROWN_CELL. Pareil si cette instance et enfant et que la mère
        et ces enfants ont un état HIT_CELL
        retourne true si on a changé DROWN_CELL, sinon false
    """
    def __init__(self, size, parent=None):
        self.parent = parent
        self.size = size
        self.child = []
        self.state = BOAT_CELL
        if parent is None:
            self.ini_boat()

    def ini_boat(self):
        for i in range(self.size - 1):
            self.child.append(Boat(self.size, parent=self))

    def get_state(self):
        return self.state

    def set_state(self, s):
        self.state = s

    def get_childs(self):
        return self.child

    def hit(self):
        def is_all_hits(array):
            for i in range(len(array)):
                if array[i].get_state() == BOAT_CELL:
                    return False
            return True

        def set_all_drowned(parent):
            parent.state = DROWN_CELL
            for i in range(len(parent.child)):
                parent.child[i].state = DROWN_CELL

        self.state = HIT_CELL
        if self.parent is None:
            if self.state == HIT_CELL and is_all_hits(self.child):
                set_all_drowned(self)
                return True
        else:
            if self.parent.get_state() == HIT_CELL \
                    and is_all_hits(self.parent.child):
                set_all_drowned(self.parent)
                return True
        return False


# Créer un board d'une taille size
def create_board(size):
    """
    créer un board representé par un tableau a deux dimenions de taille
    size
    """
    board = []
    for i in range(0, size):
        line = []
        for j in range(0, size):
            line.append(None)
        board.append(line)
    return board
