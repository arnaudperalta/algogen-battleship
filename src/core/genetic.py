from node import Node
from random import randint
import options as o
import node as nd
from math import floor


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
        self.shoot_nb = self.shoot_nb + 1
        if self.notify_drown or (self.current_node is not None and self.current_node.depth == nd.MAX_TREE_DEPTH):
            self.notify = False
            self.notify_drown = False
            self.inside_tree = False
            self.current_node = self.decision_tree
        else:
            if self.notify or self.inside_tree:
                if self.inside_tree:
                    if self.notify:
                        self.current_node = self.current_node.go_child_hit()
                        (x, y) = self.calc_coord()
                        self.last_coord = (x, y)
                        self.notify = False
                        return [x, y]
                    else:
                        self.current_node = self.current_node.go_child_miss()
                        (x, y) = self.calc_coord()
                        self.last_coord = (x, y)
                        return [x, y]
                else:
                    self.current_node = self.decision_tree
                    self.inside_tree = True
                    (x, y) = self.calc_coord()
                    self.last_coord = (x, y)
                    self.notify = False
                    return [x, y]
        choices = game.get_free_cells("left")
        res = choices[randint(0, len(choices) - 1)]
        x = res[0]
        y = res[1]
        self.last_coord = (x, y)
        return [x, y]

    def calc_coord(self):
        (a, b) = self.current_node.offset
        (x, y) = self.last_coord
        (x, y) = ((x + a) % o.options_grid_size, (y + b) % o.options_grid_size)
        return x, y

    def fitness(self):
        return self.shoot_nb

    def mutate(self, i=0, node=None):
        if i == 0:
            node = self.decision_tree
            i = randint(1, nd.MAX_TREE_DEPTH)
        if node.depth == i:
            node.offset = (randint(-o.options_grid_size, o.options_grid_size),
                           randint(-o.options_grid_size, o.options_grid_size))
            return
        else:
            r = randint(0, 1)
            if r == 0:
                self.mutate(i, node.go_child_hit())
            else:
                self.mutate(i, node.go_child_miss())

    @staticmethod
    def merge(idv1, idv2):
        def aux_merge(nt, t1, t2, depth):
            r = randint(0, 1)
            if r == 1:
                nt.offset = t1.offset
            else:
                nt.offset = t2.offset
            if depth < nd.MAX_TREE_DEPTH:
                aux_merge(nt.child_hit, t1.child_hit, t2.child_hit, depth + 1)
                aux_merge(nt.child_miss, t1.child_miss, t2.child_miss, depth + 1)
        tree1 = idv1.decision_tree
        tree2 = idv2.decision_tree
        new_idv = Individu(idv1.population)
        new_tree = new_idv.decision_tree
        r = randint(0, 1)
        if r == 1:
            new_tree.offset = tree1.offset
        else:
            new_tree.offset = tree2.offset
        aux_merge(new_tree.child_hit, tree1.child_hit, tree2.child_hit, 2)
        aux_merge(new_tree.child_miss, tree1.child_miss, tree2.child_miss, 2)
        return new_idv


# Classe réprésentant une population (un ensemble d'Individu)
# On associe à une population sa génération, désignant son avancé génétique
class Population:
    def __init__(self, size):
        # Le numéro de la génération
        self.generation = 0
        # Le tableau ou seront stocké les Individus
        self.idv_tab = []

        self.gen_fit_score = []
        for i in range(size):
            self.idv_tab.append(Individu(self))

    def get_idv(self, index):
        # TODO gestion erreur
        return self.idv_tab[index]

    def rmv_idv(self, index):
        # TODO gestion erreur
        self.idv_tab.pop(index)

    def mutate(self):
        bool_tab = [0] * len(self.idv_tab)
        n = floor((o.options_mutation_chance / 100) * len(self.idv_tab))
        for i in range(n):
            r = randint(0, len(self.idv_tab) - 1)
            while bool_tab[r] == 1 :
                r = randint(0, len(self.idv_tab) - 1)
            self.idv_tab[r].mutate()
            bool_tab[r] = 1
        return 0