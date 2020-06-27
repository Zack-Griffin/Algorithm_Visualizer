class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.is_start = False
        self.is_finish = False
        self.is_wall = False
        self.node = None

    def draw(self, canvas, x, y, node_size):
        self.node = canvas.create_rectangle([(x, y), (x+node_size, y+node_size)], fill='white', tags="node")
        self.x = x // node_size
        self.y = y // node_size