import tkinter as tk
import node as n

#setting up window
root = tk.Tk()
root.title("Visualizer")
root.resizable(False, False)
WIDTH = 750
HEIGHT = 750
#creating list to hold all nodes
node_size = 25
node_list = [list(range(WIDTH//node_size)) for i in range(HEIGHT//node_size)]
#creating global start and end nodes to store
start = n.Node()
end = n.Node()
#setting up canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack(expand=False)

def create_menu():
    #create menu object
    menu = tk.Menu(root)
    root.config(menu=menu)
    #create file object
    file = tk.Menu(menu)
    #adding commands to file object
    file.add_command(label='Set Start and Finish', command=set_Start_and_Finish)

    #adding 'file' to menu
    menu.add_cascade(label='File', menu=file)
    
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

#set start and end positions
def set_new(new_window, txt1, txt2, radio):
    #getting input x and y
    x = int(txt1.get())
    y = int(txt2.get())
    #getting selection (start or finish)
    selection = radio.get()

    #delcaring global start and end nodes to avoid reference errors
    global start
    global end
    #closing the new window
    new_window.destroy()
    new_window.update()

    #setting start or end node
    if selection == 1:
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
    elif selection == 2:
        #clearing old end node
        end.is_finish = False
        canvas.itemconfig(end.node, fill='white')

        #setting new end node and clearing old data
        end = node_list[x-1][y-1]
        end.is_finish = True
        end.is_wall = False
        end.is_start = False

        #change color of node to red
        canvas.itemconfig(end.node, fill='red')

def set_Start_and_Finish():
    #setting up new window
    new_window = tk.Toplevel(root)
    new_window.geometry("200x125")
    new_window.title("NewPos")
    new_window.resizable(False, False)
    
    #variable for radio button
    var = tk.IntVar()
    var.set(0)

    #setting up radio buttons
    start_rad = tk.Radiobutton(new_window, text="Start", variable=var, value=1)
    start_rad.place(x=25, y = 5)
    finish_rad = tk.Radiobutton(new_window, text="Finish", variable=var, value=2)
    finish_rad.place(x=100, y = 5)

    #setting up text labels
    xlabel = tk.Label(new_window, text="x:")
    xlabel.place(x=10, y=30)
    ylabel = tk.Label(new_window, text="y:")
    ylabel.place(x=10, y=55)

    #setting up input text boxes
    box1 = tk.Entry(new_window, width=25)
    box1.place(x=25, y=30)
    box2 = tk.Entry(new_window, width=25)
    box2.place(x=25, y=55)

    #setting up 'enter' button
    button = tk.Button(new_window, text="Enter", command=lambda: set_new(new_window, box1, box2, var))
    button.place(x=80, y=90)

def main():
    canvas.tag_bind("node", "<B1-Motion>", draw_wall)
    draw_nodes()
    create_menu()




    root.mainloop()
    


main()