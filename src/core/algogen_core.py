from genetic import Population
import options as o

# Etats des cellules
EMPTY_CELL = 0
BOAT_CELL = 1
HIT_CELL = 2
DROWN_CELL = 3
MISS_CELL = 4
# Phases de jeu
BOATS_PLACEMENT = 0
ATTACK = 1
PLAYER_LEFT_WIN = 2
PLAYER_RIGHT_WIN = 3


class Core:
    def __init__(self):
        # Lecture des paramètres
        self.pop = Population(o.options_nbr_idv)
        self.bot = self.pop.get_idv(0)

    def train(self):
        return 0

    def play(self, game, to_attack="left"):
        return game.attack(to_attack, self.bot.play(game, to_attack))


# Classe simulant une partie
class Game:
    def __init__(self):
        self.game_state = BOATS_PLACEMENT
        self.board1 = create_board(o.options_grid_size)
        self.board2 = create_board(o.options_grid_size)
        self.place_boat("right", [0, 0], 3, "Sud")

    # Place le bateau en crééant plusieurs fois une instance de boat sur un board, renvoie true si
    # le bateau a bien été placé
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
                if board[coords[0]][coords[1] - i] is not None or coords[1] - i < 0:
                    return False
                boat_coords.append([coords[0], coords[1] - i])
        elif orientation == "Ouest":
            for i in range(boat_size):
                if board[coords[0] - i][coords[1]] is not None or coords[0] - i < 0:
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
            board[boat_coords[i + 1][0]][boat_coords[i + 1][1]] = childs[i]
        return True

    def attack(self, board_name, coords):
        if board_name == "left":
            board = self.board1
        else:
            board = self.board2
        target = board[coords[0]][coords[1]]
        if target is None:
            board[coords[0]][coords[1]] = MISS_CELL
            return False
        if not isinstance(target, Boat) or target.state != BOAT_CELL:
            return None
        if target.hit():
            for i in range(len(board)):
                for j in range(len(board)):
                    if isinstance(board[i][j], Boat) and board[i][j].state == BOAT_CELL:
                        return False
        return True

    # Renvoie un plateau avec des valeurs prêtes pour le module d'affichage
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

    # Verifie si un bateau est placé pour chaque joueur et renvoie true si la partie commence
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
                if board[i][j] is None or isinstance(board[i][j], Boat) and board[i][j].state == BOAT_CELL:
                    cells.append([i, j])
        return cells


# Classe qui a uné définition récursive, les enfants pointent vers le parent.
class Boat:
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
        else:
            if self.parent.get_state() == HIT_CELL and is_all_hits(self.parent.child):
                set_all_drowned(self.parent)
        return True


def create_board(size):
    board = []
    for i in range(0, size):
        line = []
        for j in range(0, size):
            line.append(None)
        board.append(line)
    return board
