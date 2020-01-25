import json
from node import Node


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
        with open('././cfg/option.json', 'r') as file:
            data = json.load(file)
        # nbr de génération de la population
        self.nbr_gen = data["nbr_gen"]
        self.saved_percentage = data["saved_%"]
        self.mutation_chance = data["mut_%"]
        self.def_gen = data["def_gen"]
        self.nbr_idv = data["nbr_idv"]
        self.grid_size = data["grid_size"]
        file.close()
        # génération actuelle
        self.curr_gen = 0
        self.idv_tab = []
        for i in range(self.nbr_idv):
            k = Individu(self)
            k.hit_tree = Node(None, 0, 0)
            k.hit_tree.build_tree(10, self.grid_size)
            self.idv_tab.append(k)

    def get_idv(self, index):
        #TODO gestion erreur
        return self.idv_tab[index]

    def rmv_idv(self, index):
        # TODO gestion erreur
        self.idv_tab.pop(index)

