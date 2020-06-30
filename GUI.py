from tkinter import *
from node import Node as n

class Window():
    def __init__(self, master, h, w):

        self.master = master
        self.h = h
        self.w = w

        #setting up canvas
        self.canvas = Canvas(master, height=h, width=w)
        self.canvas.pack()

        #node items
        self.node_list = [list(range(w//n.node_size)) for i in range(h//n.node_size)]
        self.start = n()
        self.end = n()

        #setting up menu and GUI
        #create menu object
        self.menu = Menu(self.master)
        self.__create_menu()
        self.__draw_nodes()

    def __create_menu(self):
        #variable for radio button
        var = IntVar()
        var.set(0)
        #add menu object
        self.master.config(menu=self.menu)
        #create draw object
        draw = Menu(self.menu)
        #adding commands to draw object
        draw.add_radiobutton(label='Draw wall', variable=var, value=1, command=lambda: self.__set_bindings(var))
        draw.add_radiobutton(label='Erase Wall', variable=var, value=4, command=lambda: self.__set_bindings(var))
        draw.add_radiobutton(label='Set Start', variable=var, value=2, command=lambda: self.__set_bindings(var))
        draw.add_radiobutton(label='Set Finish', variable=var, value=3, command=lambda: self.__set_bindings(var))
        
        #adding 'draw' to menu
        self.menu.add_cascade(label='Draw', menu=draw)
        self.menu.add_command(label="ResetSearch", command=self.__clear_search)
        self.menu.add_command(label="Clear", command=self.__clear)
 

    #drawing each node on gui
    def __draw_nodes(self):
        i = 0
        #fills window with nodes at intervales of the square size to make grid
        for y in range(0, self.h, n.node_size):
            j = 0
            #draw each node at x,y
            for x in range(0, self.w, n.node_size):
                #create node object
                node = n()
                node.x = j
                node.y = i
                #draw node
                node.node = self.canvas.create_rectangle([(x, y), (x+n.node_size, y+n.node_size)], fill='white', tags="node")
                #add node to list
                self.node_list[j][i] = node
                j+=1         
            i+=1

    def __set_bindings(self, var):
        #resettting bindings
        self.canvas.tag_unbind("node", "<B1-Motion>")
        self.canvas.unbind("<Button-1>")

        #setting new bindings based off selection
        if var.get() == 1:
            self.canvas.tag_bind("node", "<B1-Motion>", self.__draw_wall)
        elif var.get() == 2:
            self.canvas.bind("<Button-1>", self.__set_start)
        elif var.get() == 3:
            self.canvas.bind("<Button-1>", self.__set_finish)
        else:
            self.canvas.tag_bind("node", "<B1-Motion>", self.__erase_wall)
    
    def __erase_wall(self, event):
        # getting closest node in list by dividing the
        # x and y pixel cords by the size of each node
        x = event.x // n.node_size
        y = event.y // n.node_size

        try:
            #getting node
            node = self.node_list[x][y]
            #if not start or finish node then draw wall
            if not node.is_start and not node.is_finish:
                #set to wall
                node.is_wall = False
                #change color of node to black
                self.canvas.itemconfig(node.node, fill='white')
        except IndexError:
            # this prevents errors from printing
            # to terminal when drawing out of bounds
            pass

    def __draw_wall(self, event):
        # getting closest node in list by dividing the
        # x and y pixel cords by the size of each node
        x = event.x // n.node_size
        y = event.y // n.node_size
        
        try:
            #getting node
            node = self.node_list[x][y]
            #if not start or finish node then draw wall
            if not node.is_start and not node.is_finish:
                #set to wall
                node.is_wall = True
                #change color of node to black
                self.canvas.itemconfig(node.node, fill='black')
        except IndexError:
            # this prevents errors from printing
            # to terminal when drawing out of bounds
            pass
    
    def __set_start(self, event):
        # getting closest node in list by dividing the
        # x and y pixel cords by the size of each node
        x = event.x // n.node_size
        y = event.y // n.node_size

        self.start.is_start = False
        self.canvas.itemconfig(self.start.node, fill='white')
        
        #setting new start node and clearing old data
        self.start = self.node_list[x][y]
        self.start.is_start = True
        self.start.is_wall = False
        self.start.is_finish = False

        #change color of node to green
        self.canvas.itemconfig(self.start.node, fill='green')

    def __set_finish(self, event):
        # getting closest node in list by dividing the
        # x and y pixel cords by the size of each node
        x = event.x // n.node_size
        y = event.y // n.node_size

        #clearing old end node
        self.end.is_finish = False
        self.canvas.itemconfig(self.end.node, fill='white')

        #setting new end node and clearing old data
        self.end = self.node_list[x][y]
        self.end.is_finish = True
        self.end.is_wall = False
        self.end.is_start = False

        #change color of node to red
        self.canvas.itemconfig(self.end.node, fill='red')
    
    def __clear(self):
        #resetting node list, clearing canvas, and redrawing nodes
        self.canvas.delete("all")
        self.__draw_nodes()
        
    def __clear_search(self):
        #clears current search by resetting serached nodes
        for y in self.node_list:
            for i in y:
                if i.is_searched:
                    i.is_searched = False
                    i.parent_node = None
                    i.move_cost = 0
                    i.estimate_cost = 0
                    i.sum_cost = 0
                    if not i.is_start and not i.is_finish:
                        self.canvas.itemconfig(i.node, fill="white")

    def trace_path(self, node):
        #getting parent node of finish
        n = node.parent_node
        #coloring trace path to start node
        while not n.is_start:
            self.canvas.itemconfig(n.node, fill="yellow")
            n = n.parent_node
    
    def new_text_window(self, text, font):
        #setting up new window
        newWindow = Toplevel(self.master)  
        newWindow.geometry("200x50")
        newWindow.title("Error")
        newWindow.resizable(False, False)
        #setting up text
        Label(newWindow, text=text, font=font).pack()
        #setting up button
        button = Button(newWindow, text="OK", command=newWindow.destroy)
        button.place(x=140, y=30)
        button.pack()
