import tkinter as tk
import node as n
import operator
from time import sleep


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

#creating global storage variables 
start = n.Node()
end = n.Node()
search_list = []
done = False

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
    draw.add_radiobutton(label='Draw wall', variable=var, value=1, command=lambda: set_bindings(var))
    draw.add_radiobutton(label='Erase Wall', variable=var, value=4, command=lambda: set_bindings(var))
    draw.add_radiobutton(label='Set Start', variable=var, value=2, command=lambda: set_bindings(var))
    draw.add_radiobutton(label='Set Finish', variable=var, value=3, command=lambda: set_bindings(var))
    
    #adding 'draw' to menu
    menu.add_cascade(label='Draw', menu=draw)
    menu.add_command(label="Start", command=lambda: a_star(done, search_list))
    menu.add_command(label="Clear", command=lambda: clear(done))
    
def set_bindings(var):
    #resettting bindings
    canvas.tag_unbind("node", "<B1-Motion>")
    canvas.unbind("<Button-1>")

    #setting new bindings based off selection
    if var.get() == 1:
        canvas.tag_bind("node", "<B1-Motion>", draw_wall)
    elif var.get() == 2:
        canvas.bind("<Button-1>", set_start)
    elif var.get() == 3:
        canvas.bind("<Button-1>", set_finish)
    else:
        canvas.tag_bind("node", "<B1-Motion>", erase_wall)

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

def erase_wall(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // node_size
    y = event.y // node_size
    node = node_list[x][y]

    #if not start or finish node then draw wall
    if not node.is_start and not node.is_finish:
        #set to wall
        node.is_wall = False
        #change color of node to black
        canvas.itemconfig(node.node, fill='white')

def draw_wall(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // node_size
    y = event.y // node_size
    node = node_list[x][y]

    #if not start or finish node then draw wall
    if not node.is_start and not node.is_finish:
        #set to wall
        node.is_wall = True
        #change color of node to black
        canvas.itemconfig(node.node, fill='black')

def set_start(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // node_size
    y = event.y // node_size

    #clearing old start node
    node = node_list[start.x][start.y]
    if node in search_list:
        search_list.remove(node)
        node.is_start = False
        node.is_searched = False
        canvas.itemconfig(node.node, fill='white')
    
    #setting new start node and clearing old data
    node = node_list[x][y]
    node.is_start = True
    node.is_wall = False
    node.is_finish = False
    node.is_searched = True
    #adding to search list for a-star
    search_list.append(node)
    start.copy(node)

    #change color of node to green
    canvas.itemconfig(start.node, fill='green')

def set_finish(event):
    # getting closest node in list by dividing the
    # x and y pixel cords by the size of each node
    x = event.x // node_size
    y = event.y // node_size

    #clearing old end node
    node = node_list[end.x][end.y]
    node.is_finish = False
    canvas.itemconfig(node.node, fill='white')

    #setting new end node and clearing old data
    node = node_list[x][y]
    node.is_finish = True
    node.is_wall = False
    node.is_start = False

    #change color of node to red
    canvas.itemconfig(node.node, fill='red')
    end.copy(node)

def get_successors(q):
    successors = []

    #validity checking (if in bounds and not a wall or not searched)
    if q.x+1 < len(node_list):
        node = node_list[q.x+1][q.y]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.x-1 >= 0:
        node = node_list[q.x-1][q.y]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.y+1 < len(node_list):
        node = node_list[q.x][q.y+1]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.y-1 >= 0:
        node = node_list[q.x][q.y-1]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    
    #updating info
    for x in successors:
        #setting parent (where it came from)
        x.parent_node = q
        #updating the number of moves this node is from the start node (parent moves +1)
        x.move_cost = q.move_cost + 1
        #setting this node as searched
        x.is_searched = True
        #estimating number of steps till end
        x.estimate_cost = abs(x.x - end.x) + abs(x.y - end.y)
        #storing number of steps taken plus predicted steps till end for total movement
        #cost of this path
        x.sum_cost = x.move_cost + x.estimate_cost

    return successors

def trace_path(node):
    #getting parent node of finish
    n = node.parent_node
    #coloring trace path to start node
    while not n.is_start:
        canvas.itemconfig(n.node, fill="yellow")
        n = n.parent_node

def a_star(done, search_list):

    if not done:
        #sorting list by sum cost to get next lowest
        search_list.sort(key=operator.attrgetter("sum_cost"))
        #removing from list and setting as current node
        current = search_list.pop(0)
        #getting successors of current node
        s = get_successors(current)
        #adding successors to search list
        search_list += s
        #search through all valid successors
        for i in s:
            #if is finish node
            if i.is_finish:
                #set done flag 
                done = True
                #trace parent path back to start
                trace_path(i)
                #break from loop 
                break
            #color blue to visually mark as searched
            canvas.itemconfig(i.node, fill="blue")

        root.after(10, lambda: a_star(done, search_list))


def bfs():
    pass

def clear(done):
    #resetting node list, clearing canvas, and redrawing nodes
    node_list = [list(range(WIDTH//node_size)) for i in range(HEIGHT//node_size)]
    canvas.delete("all")
    draw_nodes()
    done = False
    search_list.clear()


def main():
    draw_nodes()
    create_menu()
    root.mainloop()
main()