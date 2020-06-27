import tkinter as tk
import node as n

#setting up window
window = tk.Tk()
window.title("Visualizer")
WIDTH = 750
HEIGHT = 750
#creating list to hold all nodes
node_size = 25
node_list = [list(range(WIDTH//node_size)) for i in range(HEIGHT//node_size)]
#setting up canvas
canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack()

def create_menu():
    #create menu object
    menu = tk.Menu(window)
    window.config(menu=menu)
    #create file object
    file = tk.Menu(menu)
    #adding commands to file object
    file.add_command(label='Set Start and Finish', command=set_Start_and_Finish)
    file.add_command(label='Exit', command=client_exit)
    #adding 'file' to menu
    menu.add_cascade(label='File', menu=file)


def draw_nodes(event=None):
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

    #if not start or finish node then draw wall
    if not node.is_start:
        if not node.is_finish:
            #set to wall
            node.is_wall = True
            #change color of node to black
            canvas.itemconfig(node.node, fill='black')
            
#exit the app
def client_exit():
    exit()

def set_Start_and_Finish():
    pass

def main():
    canvas.tag_bind("node", "<B1-Motion>", draw_wall)
    draw_nodes()
    create_menu()




    window.mainloop()
    


main()