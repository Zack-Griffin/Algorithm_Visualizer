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

def a_star(done, app):
    if not done:
        #sorting list by sum cost to get next lowest
        app.search_list.sort(key=operator.attrgetter("sum_cost"))
        #removing from list and setting as current node
        current = app.search_list.pop(0)

        #getting successors of current node
        s = get_successors(current, app)
        #adding successors to search list
        app.search_list += s

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

        app.master.after(10, lambda: a_star(done, app))


def bfs():
#     pass

def main():
    #setting up main window
    root = tk.Tk()
    root.title("Visualizer")
    root.resizable(False, False)
    #setting height and width
    WIDTH = 750
    HEIGHT = 750

    done = False
    #creating app
    app = GUI.Window(root, HEIGHT, WIDTH)

    #created button for new algotithm
    app.menu.add_command(label="A-star", command=lambda: a_star(done, app))

    #starting event loop
    root.mainloop()

main()
    