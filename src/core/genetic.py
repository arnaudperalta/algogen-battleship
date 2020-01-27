from node import Node
import options as o


class Individu:
    def __init__(self, p):
        # ensemble de décision après un tir
        self.hit_tree = None
        # population correspondant à l'individu
        self.population = p

    def get_all_hit_tree(self):
        return self.hit_tree


   # TODO MUTATION ET REPRODUCTION


class Population:
    def __init__(self):
        # génération actuelle
        self.curr_gen = 0
        self.idv_tab = []
        for i in range(o.options_nbr_idv):
            k = Individu(self)
            k.hit_tree = Node(None, 0, 0)
            k.hit_tree.build_tree(10, o.options_grid_size)
            self.idv_tab.append(k)

    def get_idv(self, index):
        #TODO gestion erreur
        return self.idv_tab[index]

    def rmv_idv(self, index):
        # TODO gestion erreur
        self.idv_tab.pop(index)

