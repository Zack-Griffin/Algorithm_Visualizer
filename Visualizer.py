import tkinter as tk
import node as n

#setting up window
root = tk.Tk()
root.title("Visualizer")
root.resizable(False, False)
WIDTH = 750
HEIGHT = 750

#setting up canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#creating list to hold all nodes
node_size = 25
node_list = [list(range(WIDTH//node_size)) for i in range(HEIGHT//node_size)]

#creating global storage variables for start and end nodes 
#TODO: might be better to simply clear board when changing nodes instead of storing them 
start = n.Node()
end = n.Node()

def create_menu():
    #variable for radio button
    var = tk.IntVar()
    var.set(0)
    #create menu object
    menu = tk.Menu(root)
    root.config(menu=menu)
    #create draw object
    draw = tk.Menu(menu)
    #adding commands to draw object
    draw.add_radiobutton(label='Wall', variable=var, value=1, command=lambda: set_bindings(var))
    draw.add_radiobutton(label='Set Start', variable=var, value=2, command=lambda: set_bindings(var))
    draw.add_radiobutton(label='Set Finish', variable=var, value=3, command=lambda: set_bindings(var))
    #adding 'draw' to menu
    menu.add_cascade(label='Draw', menu=draw)
    
def set_bindings(var):
    canvas.tag_unbind("node", "<B1-Motion>")
    canvas.unbind("<Button-1>")

    if var.get() == 1:
        canvas.tag_bind("node", "<B1-Motion>", draw_wall)
    elif var.get() == 2:
        canvas.bind("<Button-1>", set_start)
    else:
        canvas.bind("<Button-1>", set_finish)

def draw_nodes(event=None):
    i = 0
    #fills window with nodes at intervales of the square size to make grid
    for y in range(0, HEIGHT, node_size):
        j = 0
        #draw each node at x,y
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

    #if not start or finish node then draw wall
    if not node.is_start:
        if not node.is_finish:
            #set to wall
            node.is_wall = True
            #change color of node to black
            canvas.itemconfig(node.node, fill='black')

def set_start(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // 25
    y = event.y // 25
    #delcaring global start node to avoid reference errors
    global start
    
    #clearing old start node
    start.is_start = False
    canvas.itemconfig(start.node, fill='white')
    
    #setting new start node and clearing old data
    start = node_list[x][y]
    start.is_start = True
    start.is_wall = False
    start.is_finish = False

    #change color of node to green
    canvas.itemconfig(start.node, fill='green')

def set_finish(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // 25
    y = event.y // 25

    #delcaring global end node to avoid reference errors
    global end

    #clearing old end node
    end.is_finish = False
    canvas.itemconfig(end.node, fill='white')

    #setting new end node and clearing old data
    end = node_list[x][y]
    end.is_finish = True
    end.is_wall = False
    end.is_start = False

    #change color of node to red
    canvas.itemconfig(end.node, fill='red')

def a_star():
    pass

def bfs():
    pass

def main():
    draw_nodes()
    create_menu()

    root.mainloop()
    #TODO: add function to reset grid after searching


main()