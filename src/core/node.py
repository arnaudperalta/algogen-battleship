from random import randint
import options as o

MAX_TREE_DEPTH = 10


class Node:
    def __init__(self, previous=None, offset=(0, 0), depth=1):
        self.parent = previous
        self.depth = depth
        # Couple d'entier representant un offset par rapport au coords du premier tir
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
            self.child_hit = Node(self, offset=(randint(-grid_size, grid_size), randint(-grid_size, grid_size)),
                                  depth=self.depth + 1)
            self.child_miss = Node(self, offset=(randint(-grid_size, grid_size), randint(-grid_size, grid_size)),
                                   depth=self.depth + 1)
