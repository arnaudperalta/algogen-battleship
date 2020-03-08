from random import randint
import options as o

MAX_TREE_DEPTH = 10


class Node:
    """
    Classe simulant un noeud au sein d'un arbre de décision, un noeud
    est muni d'un offset et de deux références vers d'autre noeuds.
    Une branche sera pour le cas où l'individu ratera un tir, et une
    autre branche pour quand le tir sera réussi.

    Attributs
    ---------
    parent
        Référence vers le noeud parent
    depth
        Profondeur dans laquel se trouve le noeud par rapport à l'arbre
    offset
        Couple d'entiers representant un offset par rapport aux
        coordonéees du premier tir
    child_hit
        Branche exploré dans le cas où l'individu réussi son tir
    child_miss
        Branche exploré dans le cas où l'individu rate son tir

    Méthodes
    --------
    go_child_hit()
        Retourne la référence du noeud child_hit
    go_child_miss()
        Retourne la référence du noeud child_miss
    go_backward()
        Retourne la référence du noeud parent
    build_tree()
        Méthode appellé dans le constructeur pour instancier deux fils
        Noeud à cette instance dans le cas ou depth n'a pas atteint
        MAX_TREE_DEPTH
    """
    def __init__(
            self,
            previous=None,
            offset=(
                    randint(-o.options_grid_size, o.options_grid_size),
                    randint(-o.options_grid_size, o.options_grid_size)),
            depth=1):
        self.parent = previous
        self.depth = depth
        # Couple d'entier representant un offset par
        # rapport au coords du premier tir
        self.offset = offset
        self.child_hit = None
        self.child_miss = None
        self.build_tree(o.options_grid_size)

    def go_child_hit(self):
        return self.child_hit

    def go_child_miss(self):
        return self.child_miss

    def go_backward(self):
        return self.parent

    def build_tree(self, grid_size):
        if self.depth < MAX_TREE_DEPTH:
            self.child_hit = Node(
                self,
                offset=(
                    randint(-grid_size, grid_size),
                    randint(-grid_size, grid_size)),
                depth=self.depth + 1)
            self.child_miss = Node(
                self,
                offset=(randint(-grid_size, grid_size),
                        randint(-grid_size, grid_size)),
                depth=self.depth + 1)
