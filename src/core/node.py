from random import randint


class Node:
    def __init__(self, pn, x, y):
        # noeud précédent
        self.prevNode = pn
        # drapeau indiquant l'état de la node
        self.flag = "STANDBY"
        # coordonnées du noeud dans la grille
        self.coordx = x
        self.coordy = y
        # branche suivante
        self.next_hit_node = None
        self.next_miss_node = None

    # on met a jour le drapeau avec la grille de jeu(tir effectif)
    def change_node_status(self, s):
        if s == "HIT":
            self.flag = "HIT"
        else:
            self.flag = "MISSED"

    # fonction pour accéder à un autre noeud
    # TODO le dépassement de coordonnées est pour l'instant gérer avec des modulos a voir pour changer plus tard
    def go_to_next_node(self):
        # on vérifie si un tir à eu lieu sur le noeud courant d'abord
        if self.flag == "NEUTRAL" :
            print("shoot before moving to next node")
            return
        if self.flag == "MISSED" :
            return self.next_miss_node
        else:
            return self.next_hit_node

    def go_backward(self):
        return self.prevNode

    def build_tree(self, max_tree_depth, grid_size):
        if max_tree_depth == 0:
            return
        else:
            hit = Node(self, randint(-grid_size, grid_size), randint(-grid_size, grid_size))
            self.next_hit_node = hit
            hit.build_tree(max_tree_depth - 1, grid_size)
            miss = Node(self, randint(-grid_size, grid_size), randint(-grid_size, grid_size))
            self.next_miss_node = miss
            miss.build_tree(max_tree_depth - 1, grid_size)
