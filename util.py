import math
import random
import numpy as np
from graphics import *

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
    graph = {}
    # Use a while loop to avoid skipping stitches if repeats happen
    i = 0
    while i < num_front_stitches:
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
            # Increment i
            i += 1

    return graph

"""
Helper function: get distance between edge (which is a tuple of 2 coordinates)
"""
def get_edge_length(edge):
        # Assume a edge is a tuple of 2 tuples ((a,b), (c,d))
        x_diff = edge[0][0] - edge[1][0]
        y_diff = edge[0][1] - edge[1][1]
        return math.sqrt(x_diff**2 + y_diff**2)

"""
Helper function: consistently format edges given 2 vertices
"""
def get_formatted_edge(v1, v2):
    # Ensure uniqueness by ordering coordinates: <x, then <y if x's same
    if v1[0] < v2[0]:
        edge = (v1, v2)
    elif v1[0] > v2[0]:
        edge = (v2, v1)
    else:
        if v1[1] < v2[1]:
            edge = (v1, v2)
        elif v1[1] > v2[1]:
            edge = (v2, v1)
        else:
            print('ERROR! Caught a self loop')
            print(v1, v2)
            exit(0)
    return edge

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