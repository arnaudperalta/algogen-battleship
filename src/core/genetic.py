import json
from random import randint, choice


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
        self.def_tree.insert(prop, (x_offset, y_offset))

    def set_hit_tree(self, x_offset, y_offset, prop):
        self.hit_tree.insert(prop, (x_offset, y_offset))

    # ajout d'un gène aléatoire (dans le def_tree ou le hit_tree) avec une prioriété aléatoire
    def pos_mutate(self):
        v = choice([True, False])
        x = randint(-self.grid_size, self.grid_size)
        y = randint(-self.grid_size, self.grid_size)
        if v:
            k = randint(0, len(self.def_tree) - 1)
            self.set_def_tree(x, y , k)
        else:
            k = randint(0, len(self.hit_tree) - 1)
            self.set_hit_tree(x, y, k)

    # suppression d'un gène TODO tj le dernier pour l'instant a voir pour changer plus tard
    def neg_mutate(self):
        v = choice([True, False])
        if v:
            self.def_tree.pop(len(self.def_tree) - 1)
        else:
            self.hit_tree.pop(len(self.hit_tree) - 1)

    # nbr de gène total de l'individu
    def gene_count(self):
        return len(self.def_tree) + len(self.hit_tree)

    @staticmethod
    def merge(idv1, idv2):
        new_idv = Individu()
        l1 = max(len(idv1.def_tree), len(idv2.def_tree))
        l2 = max(len(idv1.hit_tree), len(idv2.hit_tree))
        for i in range(l1):
            if i >= len(idv1.def_tree):
                (k, l) = idv2.get_def_tree(i)
                new_idv.set_def_tree(k, l, i)
                continue
            if i >= len(idv2.hit_tree):
                (x, y) = idv1.get_def_tree(i)
                new_idv.set_def_tree(x, y, i)
                continue
            (x, y) = idv1.get_def_tree(i)
            (k, l) = idv2.get_def_tree(i)
            v = choice([True, False])
            if v:
                new_idv.set_def_tree(x, y, i)
                new_idv.set_def_tree(k, l, i + 1)
            else:
                new_idv.set_def_tree(k, l, i)
                new_idv.set_def_tree(x, y, i + 1)


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
            k = Individu()
            for j in range(self.def_gen):
                k.set_def_tree(randint(-self.grid_size, self.grid_size), randint(-self.grid_size, self.grid_size), j)
                k.set_hit_tree(randint(-self.grid_size, self.grid_size), randint(-self.grid_size, self.grid_size), j)
            self.idv_tab.append(k)





