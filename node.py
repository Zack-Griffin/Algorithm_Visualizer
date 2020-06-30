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
        #info for pathfinding
        self.move_cost = 0
        self.estimate_cost = 0
        self.sum_cost = 0
        self.parent_node = None
        self.is_searched = False