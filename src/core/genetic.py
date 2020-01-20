import json
from random import randint


class Individu:
    def __init__(self):
        # ensemble de décision par défault
        self.def_tree = []
        # ensemble de décision après un tir
        self.hit_tree = []

    def get_def_tree(self, prop):
        return self.def_tree[prop]

    def get_hit_tree(self, prop):
        return self.hit_tree[prop]

    def set_def_tree(self, x_offset, y_offset, prop):
        if prop > len(self.def_tree):
            self.def_tree.append((x_offset, y_offset))
        else:
            self.def_tree.insert(prop, (x_offset, y_offset))

    def set_hit_tree(self, x_offset, y_offset, prop):
        if prop > len(self.hit_tree):
            self.hit_tree.append((x_offset, y_offset))
        else:
            self.hit_tree.insert(prop, (x_offset, y_offset))


class Population:
    def __init__(self):
        with open('./cfg/option.json', 'r') as file:
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
            k = Individu()
            for j in range(self.def_gen):
                k.set_def_tree(randint(-self.grid_size, self.grid_size), randint(-self.grid_size, self.grid_size), j)
                k.set_hit_tree(randint(-self.grid_size, self.grid_size), randint(-self.grid_size, self.grid_size), j)
            self.idv_tab.append(k)


