import importlib
from graphics import *
util = importlib.import_module('util')
decision = importlib.import_module('decision')
optimization = importlib.import_module('optimization')

# Generate a random instance of a stitching pattern
# create a window
m = 3
n = 5
win = GraphWin(width = 200, height = 200)
# set the coordinates of the window
# bottom left is (0, 0) and top right is (m, n)
win.setCoords(0, 0, m, n)

graph = util.random_pattern(m, n)
# Print out the graph in a pretty-ish manner
for vertex in graph:
    print(vertex, graph[vertex])
    pt1 = Point(vertex[0], vertex[1])
    pt1.draw(win)
    for edge in graph[vertex]:
        pt2 = Point(edge[0], edge[1])
        pt2.draw(win)
        line = Line(pt1, pt2)
        line.draw(win)

# Pause before closing
win.getMouse()
win.close()
