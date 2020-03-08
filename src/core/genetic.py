from node import Node
import random as rd
import options as o
import node as nd
from math import floor


class Individu:
    """
    Classe simulant un individu au sein d'une population.

    Attributs
    ---------
    population
        Référence vers une instance de Population où est extrait
        l'individu
    decision_tree
        Arbre de décision, l'individu parcourera l'arbre de décision
        pour choisi où tirer, il se dirigera dans la branche de gauche
        si son tir précédent à toucher, droite si rater. Si le bateau
        ciblé coule, on quitte l'arbre
    current_node
        Référence sur le noeud actuel dans l'arbre de décision
    notify
        ...
    notify_drown
        ...
    inside_tree
        Booléen indiquant si l'IA parcourt l'arbre de décision ou non
    last_coord
        Coordonnées de la dernière frappe
    shoot_nb
        Nombre de tir tiré au cours de la partie actuel

    Methodes
    --------
    play(game)
        Joue un coup dans l'instance de Game donné en paramètre
        Il jouera un coup au hasard sur la grille puis une fois une case
        touchée, il choisira ou tira grâce à son arbre de décision
        jusqu'a ce qu'il coule.
    calc_coord()
        Détermine les coordonnées où tirer grâce aux offset determiné
        par l'arbre des decisions
    fitness()
        Retourne le résultat de la fonction d'évaluation sur cet
        individu (son nombre de coup joué)
    mutate(i, node)
        ???
        TODO: mettre un nom de paramètre claire
    """
    def __init__(self, pop):
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
        if self.notify_drown \
                or (self.current_node is not None
                    and self.current_node.depth == nd.MAX_TREE_DEPTH):
            self.notify = False
            self.notify_drown = False
            self.inside_tree = False
            self.current_node = self.decision_tree
        else:
            if self.notify or self.inside_tree:
                if self.inside_tree:
                    if self.notify:
                        self.current_node \
                            = self.current_node.go_child_hit()
                        (x, y) = self.calc_coord()
                        self.last_coord = (x, y)
                        self.notify = False
                        return [x, y]
                    else:
                        self.current_node \
                            = self.current_node.go_child_miss()
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
        res = choices[rd.randint(0, len(choices) - 1)]
        x = res[0]
        y = res[1]
        self.last_coord = (x, y)
        return [x, y]

    def calc_coord(self):
        (a, b) = self.current_node.offset
        (x, y) = self.last_coord
        (x, y) = (
            (x + a) % o.options_grid_size,
            (y + b) % o.options_grid_size
        )
        return x, y

    def fitness(self):
        return self.shoot_nb

    def mutate(self, node=None):
        r = rd.random()
        if r * 100 <= o.options_mutation_chance:
            node.offset = (rd.randint(-o.options_grid_size, o.options_grid_size),
                           rd.randint(-o.options_grid_size, o.options_grid_size))
            print("mutation :" + str(r) + " " + str(o.options_mutation_chance) )
        if node.depth < nd.MAX_TREE_DEPTH:
            self.mutate(node.go_child_hit())
            self.mutate(node.go_child_miss())


def merge(idv1, idv2):
    """
    Opération de cross-over de deux individus qui crééra une nouvelle
    instance de Individu, qui sera muni d'un arbre de décision
    inspiré des deux individus parent
    """
    def aux_merge(nt, t1, t2, depth):
        rand = rd.randint(0, 1)
        if rand == 1:
            nt.offset = t1.offset
        else:
            nt.offset = t2.offset
        if depth < nd.MAX_TREE_DEPTH:
            aux_merge(
                nt.child_hit,
                t1.child_hit,
                t2.child_hit,
                depth + 1
            )
            aux_merge(
                nt.child_miss,
                t1.child_miss,
                t2.child_miss,
                depth + 1
            )
    tree1 = idv1.decision_tree
    tree2 = idv2.decision_tree
    new_idv = Individu(idv1.population)
    new_tree = new_idv.decision_tree
    r = rd.randint(0, 1)
    if r == 1:
        new_tree.offset = tree1.offset
    else:
        new_tree.offset = tree2.offset
    aux_merge(
        new_tree.child_hit,
        tree1.child_hit,
        tree2.child_hit,
        2
    )
    aux_merge(
        new_tree.child_miss,
        tree1.child_miss,
        tree2.child_miss,
        2
    )
    return new_idv


class Population:
    """
    Classe simulant un ensemble d'individu au sein d'un algorithme
    génétique nommé Population. Une population est dépendante d'un
    numéro de génération qui correspondra au degré d'évolution de
    l'espèce.

    Attributs
    ---------
    generation
        Numéro de génération, équivalent au degré d'évolution de
        l'espèce, plus il est haut, plus l'espèce est évolué et ses
        individus sont performants.
    idv_tab
        Tableau où sont stockées les références des Individus membre
        de cette Population
    gen_fit_score
        Tableau où sont stockées les résultats de la fitness pour chaque
        individu membre de la population

    Méthodes
    --------
    get_idv(index)
        Retourne l'individu à l'index 'index' dans idv_tab
    rmv_idv(index)
        Fonction utilisé lors de la suppression des individus les moins
        performants. On supprime un individu à l'index donné dans
        idv_tab
    mutate()
        Fonction de mutation pour tout les individus présent dans cette
        population, les arbres de décisions de tout les individus sont
        légèrement changés aléatoirement
    """
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
        for idv in self.idv_tab:
            idv.mutate(idv.decision_tree)
        return 0