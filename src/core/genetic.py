from node import Node
from random import randint
import options as o
import node as nd


class Individu:
    def __init__(self, pop):
        # ensemble de décision après un tir
        self.hit_tree = None
        # population correspondant à l'individu
        self.population = pop
        # Création de l'arbre de décision associé à l'individu
        self.decision_tree = Node()
        self.current_node = None
        self.notify = False
        self.notify_drown = False
        self.inside_tree = False
        self.last_coord = (0, 0)
        self.shoot_nb = 0

    def play(self, game):
        ++self.shoot_nb
        if self.notify_drown or (self.current_node is not None and self.current_node.depth == nd.MAX_TREE_DEPTH):
            self.notify = False
            self.notify_drown = False
            self.inside_tree = False
            self.current_node = self.decision_tree
        else:
            if self.notify or self.inside_tree:
                print("wtf j'ai touché")
                if self.inside_tree:
                    if self.notify:
                        self.current_node = self.current_node.go_child_hit()
                        (x, y) = self.calc_coord()
                        self.last_coord = (x, y)
                        self.notify = False
                        print(self.last_coord)
                        return [x, y]
                    else:
                        self.current_node = self.current_node.go_child_miss()
                        (x, y) = self.calc_coord()
                        self.last_coord = (x, y)
                        print(self.last_coord)
                        return [x, y]
                else:
                    self.current_node = self.decision_tree
                    self.inside_tree = True
                    (x, y) = self.calc_coord()
                    self.last_coord = (x, y)
                    print(self.last_coord)
                    self.notify = False
                    return [x, y]
        choices = game.get_free_cells("left")
        res = choices[randint(0, len(choices) - 1)]
        x = res[0]
        y = res[1]
        print(x, y)
        self.last_coord = (x, y)
        return [x, y]

    def calc_coord(self):
        (a, b) = self.current_node.offset
        (x, y) = self.last_coord
        (x, y) = ((x + a) % o.options_grid_size, (y + b) % o.options_grid_size)
        return x, y

    def fitness(self):
        return self.shoot_nb

    @staticmethod
    def merge(idv1, idv2):
        return 0


    # TODO MUTATION ET REPRODUCTION


# Classe réprésentant une population (un ensemble d'Individu)
# On associe à une population sa génération, désignant son avancé génétique
class Population:
    def __init__(self, size):
        # Le numéro de la génération
        self.generation = 1
        # Le tableau ou seront stocké les Individus
        self.idv_tab = []
        self.fit_tab = []
        for i in range(size):
            self.idv_tab.append(Individu(self))

    def get_idv(self, index):
        # TODO gestion erreur
        return self.idv_tab[index]

    def rmv_idv(self, index):
        # TODO gestion erreur
        self.idv_tab.pop(index)

    def mutate(self):
        return 0