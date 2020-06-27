import tkinter as tk
import node as n

#setting up window
window = tk.Tk()
WIDTH = 750
HEIGHT = 750
#creating list to hold all nodes
node_list = [list(range(WIDTH//25)) for i in range(HEIGHT//25)]
#setting up canvas
canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack()

def draw_nodes(event=None):
    #width and height for node
    node_size = 25
    
    i = 0
    #fills window with nodes at intervales of the square size
    for y in range(0, HEIGHT, node_size):
        j = 0
        #draw each ndde at x,y
        for x in range(0, WIDTH, node_size):
            #create node object
            node = n.Node()
            #draw node
            node.draw(canvas, x, y, node_size)
            #add node to list
            node_list[j][i] = node
            j+=1         
        i+=1

def draw_wall(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // 25
    y = event.y // 25
    node = node_list[x][y]

    if not node.is_start:
        if not node.is_finish:
            node.is_wall = True
            #change color of node to black
            canvas.itemconfig(node.node, fill='black')


def main():
    canvas.tag_bind("node", "<B1-Motion>", draw_wall)
    draw_nodes()

    window.mainloop()




main()