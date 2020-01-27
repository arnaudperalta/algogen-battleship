from node import Node
import options as o


class Individu:
    def __init__(self, pop):
        # ensemble de décision après un tir
        self.hit_tree = None
        # population correspondant à l'individu
        self.population = pop
        # Création de l'arbre de décision associé à l'individu
        self.decision_tree = Node()

    # TODO MUTATION ET REPRODUCTION


# Classe réprésentant une population (un ensemble d'Individu)
# On associe à une population sa génération, désignant son avancé génétique
class Population:
    def __init__(self, size):
        # Le numéro de la génération
        self.generation = 1
        # Le tableau ou seront stocké les Individus
        self.idv_tab = []
        for i in range(size):
            self.idv_tab.append(Individu(self))

    def get_idv(self, index):
        # TODO gestion erreur
        return self.idv_tab[index]

    def rmv_idv(self, index):
        # TODO gestion erreur
        self.idv_tab.pop(index)
