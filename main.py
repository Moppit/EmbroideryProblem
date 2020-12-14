import importlib
import math
import time
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')
arkin = importlib.import_module('arkin')
tsp = importlib.import_module('tsp_solver')

# Generate a random instance of a stitching pattern
# create a window
# m = 4
# n = 3

# pattern = util.random_pattern(m, n)

# TODO: write more known test cases!
# Test case 1: triangle component
pattern = {
    (2, 2): [(1, 1)],
    (1, 1): [(2, 2)],
    (1, 0): [(3, 3), (0, 0), (0, 1)],
    (3, 3): [(1, 0)],
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(0, 0), (1, 0)]
}

connected_pattern = {
    (2, 2): [(1, 1)],
    (1, 1): [(2, 2), (3,3)],
    (1, 0): [(3, 3), (0, 0), (0, 1)],
    (3, 3): [(1, 0), (1,1)],
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(0, 0), (1, 0)]
}

test = {
    (0,0): [(1,1), (0,1)],
    (1,1): [(0,0), (0,1)],
    (0,1): [(0,0), (1,1)]
}
# util.visual(m, n, pattern)

"""
Timing code
"""
# Timing DPLL
num_trials = 100
m = 5
n = 5
# int((m*n)*(m*n-1)/2) is the maximum number of stitches possible
for num_stitches in range(1, int((m*n)*(m*n-1)/2)):
    for i in range(num_trials):
        pattern = util.random_pattern(m, n, num_stitches)
        num_vertices = len(pattern)
        print('Current graph:')
        for v in pattern:
            print(v, pattern[v])

        # Create arkin approx solver
        approx = arkin.Arkin(pattern)

        # Concorde TSP Solver
        start_time = time.time()
        arkin_val = approx.approx_2()
        end_time = time.time()
        arkin_time = end_time - start_time

        # Sleep briefly for your computer's sanity
        print('Finished trial', i, 'of', num_stitches, 'stitches')

        # Write to Concorde file
        file_write = open('arkin_stitch_count.csv', 'a')
        # Format: m, n, num_stitches, num_vertices, i, time, value
        file_write.write(str(m) + ',' + str(n) + ',' + str(num_stitches) + ',' + str(num_vertices) + ',' + str(i) + ',' + str(arkin_time) + ',' + str(arkin_val) + '\n')
        file_write.close()