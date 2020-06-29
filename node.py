class Node:
    node_size = 25
    def __init__(self):
        #x and y values of the current node
        self.x = 0
        self.y = 0
        #flags to determine the type of node
        self.is_start = False
        self.is_finish = False
        self.is_wall = False
        #holds the data returned from the canvas drawing
        self.node = None
        #info for a-star
        self.move_cost = 0
        self.estimate_cost = 0
        self.sum_cost = 0
        self.parent_node = None
        self.is_searched = False

    def copy(self, node):
        self.x = node.x
        self.y = node.y
        self.is_start = node.is_start
        self.is_finish = node.is_finish
        self.is_wall = node.is_wall
        self.node = node.node
        self.move_cost = node.move_cost
        self.estimate_cost = node.estimate_cost
        self.sum_cost = node.sum_cost
        self.parent_node = node.parent_node
        self.is_searched = node.is_searched