import random
import numpy as np
from graphics import *

"""
Graph class
"""
class Node:
    def __init__(self):
        self.identifier = ''
        self.contents = None
        self.edges = []

class Graph:
    def __init__(self):
        self.graph = None

    def insert_node(self, identifier, contents):
        print('TODO: add node to graph')

"""
Generates a random instance of the embroidery problem.
Inputs:
    m: number rows in Euclidean plane
    n: number columns in Euclidean plane
    density: (defaults = 0.5) determines the ratio of stitches to non-stitched portions
Outputs: Euclidean graph
"""
def random_pattern(m, n, num_front_stitches=1):#density=0.1):
    # Create a Euclidean graph in m x n plane
    # There are at most m*n vertices, so there are at most a complete graph of front stitches
    # num_front_stitches = int((m*n)*(m*n-1)/2)
    graph = {}
    for i in range(num_front_stitches):
        # num = random.random()
        # if num < density:
        # Generate two stitching endpoints
        start_row, start_col = (np.random.choice(range(m+1)), np.random.choice(range(n+1)))
        end_row, end_col = (np.random.choice(range(m+1)), np.random.choice(range(n+1)))
        # Ensure we don't get self loops
        if (start_row, start_col) != (end_row, end_col):
            # Check if endpoints are in the graph -- add the edges
            # Start node
            if (start_row, start_col) not in graph:
                # Add new vertex if not already in graph
                graph[(start_row, start_col)] = []
            # Check if edge should be added
            if (end_row, end_col) not in graph[(start_row, start_col)]:
                graph[(start_row, start_col)].append((end_row, end_col))
            # End node
            if (end_row, end_col) not in graph:
                # Add new vertex if not already in graph
                graph[(end_row, end_col)] = []
            # Check if edge should be added
            if (start_row, start_col) not in graph[(end_row, end_col)]:
                graph[(end_row, end_col)].append((start_row, start_col))

    return graph

    # graph = [[None for _ in range(n)] for _ in range(m)]
    # print(graph)
    """
    for i in range(num_front_stitches):
        num = random.random()
        if num < density:
            # Generate two stitching endpoints
            start_row, start_col = (np.random.choice(range(n)), np.random.choice(range(m)))
            end_row, end_col = (np.random.choice(range(n)), np.random.choice(range(m)))

    TODO: Continue here! Figure out how to best structure your graph

    Node:
        key = name
        x = val
        y = val
        front_taken = []
        back_taken = []
        edges: [Node, Node, Node]

    vertex: (x, y)
    graph: {
        (x, y): [(x1, y1), (x2, y2)]
        (x1, y1): [(x, y), ]
    }

    """

# TODO: add a benchmarking utility! Would be nice to have consistent format here

# Graph visualization util
def visual(m, n, pattern):
    win = GraphWin(width = 800, height = 800)
    # set the coordinates of the window
    # bottom left is (0, 0) and top right is (m, n)
    win.setCoords(-1, -1, m+1, n+1)

    graph = pattern
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