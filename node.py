class Node:
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

    def draw(self, canvas, x, y, node_size):
        #drawing the node onto the gui
        self.node = canvas.create_rectangle([(x, y), (x+node_size, y+node_size)], fill='white', tags="node")
        #setting x and y values
        self.x = x // node_size
        self.y = y // node_size