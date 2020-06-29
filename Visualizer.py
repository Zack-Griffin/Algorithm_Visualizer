import tkinter as tk
import operator
import GUI

def get_successors(q, app):
    successors = []

    #validity checking (if in bounds and not a wall or not searched)
    if q.x+1 < len(app.node_list):
        node = app.node_list[q.x+1][q.y]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.x-1 >= 0:
        node = app.node_list[q.x-1][q.y]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.y+1 < len(app.node_list):
        node = app.node_list[q.x][q.y+1]
        if not node.is_wall and not node.is_searched:
            successors.append(node)
    if q.y-1 >= 0:
        node = app.node_list[q.x][q.y-1]
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
        x.estimate_cost = abs(x.x - app.end.x) + abs(x.y - app.end.y)
        #storing number of steps taken plus predicted steps till end for total movement
        #cost of this path
        x.sum_cost = x.move_cost + x.estimate_cost

    return successors

def a_star(done, search_list, app):

    if not app.start.is_searched:
        #clearing trasy from search list
        search_list.clear()
        #adding start node and setting it as searched
        search_list.append(app.start)
        app.start.is_searched = True

    if not done:
        try:
            #sorting list by sum cost to get next lowest
            search_list.sort(key=operator.attrgetter("sum_cost"))

            #removing start of list and setting as current node
            current = search_list.pop(0)

            #getting successors of current node
            s = get_successors(current, app)
            #adding successors to search list
            search_list += s

            #search through all valid successors
            for i in s:
                #if is finish node
                if i.is_finish:
                    #set done flag 
                    done = True
                    #trace parent path back to start
                    app.trace_path(i)
                    #break from loop 
                    break
                #color blue to visually mark as searched
                app.canvas.itemconfig(i.node, fill="blue")
            #recalling function after 10 ms
            app.master.after(10, lambda: a_star(done, search_list, app))
        except IndexError:
            #opening a text box window to display error message
            app.new_text_window("Could not find shortest path", "-*-lucidatypewriter-medium-r-*-*-*-140-*-*-*-*-*-*")

def bfs():
    pass

def main():
    #setting up main window
    root = tk.Tk()
    root.title("Visualizer")
    root.resizable(False, False)
    #setting height and width of app
    WIDTH = 750
    HEIGHT = 750
    #creating app
    app = GUI.Window(root, HEIGHT, WIDTH)

    #flag for algorithm finishing
    done = False
    search_list = []

    #created button for new algotithm
    app.menu.add_command(label="A-star", command=lambda: a_star(done, search_list, app))

    #starting event loop
    root.mainloop()

main()
    