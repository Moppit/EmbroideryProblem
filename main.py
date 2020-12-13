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

# util.visual(m, n, pattern)

# # Timing DPLL
# num_trials = 100
# m_upper = 5
# n_upper = 5
# # for m in range(3, m_upper+1):
# #     for n in range(1, n_upper+1):
# m = 5
# n = 5
# # int((m*n)*(m*n-1)/2) is the maximum number of stitches possible
# for num_stitches in range(1, int((m*n)*(m*n-1)/2)):
#     for i in range(num_trials):
#         pattern = util.random_pattern(m, n, num_stitches)
#         print('Current graph:')
#         for v in pattern:
#             print(v, pattern[v])
#         dpll_obj = dpll.DPLL(pattern)
#         dpll_obj.make_graph()
#         num_vertices = len(dpll_obj.pattern)
#         min_val = math.inf
#         start_time = time.time()
#         for vertex in list(dpll_obj.pattern.keys()):
#             start = vertex
#             new_val = dpll_obj.dpll(start, start, True, [])
#             if new_val < min_val:
#                 min_val = new_val
#         end_time = time.time()
#         file_write = open('dpll_stitch_count.csv', 'a')
#         # Format: m, n, num_stitches, num_vertices, i, time, value
#         file_write.write(str(m) + ',' + str(n) + ',' + str(num_stitches) + ',' + str(num_vertices) + ',' + str(i) + ',' + str(end_time-start_time) + ',' + str(min_val) + '\n')
#         file_write.close()
#         print('Finished trial', i, 'of', num_stitches, 'stitches')

# Testing Arkin
# approx2_obj = arkin.Arkin(pattern)
# t_approx_len = approx2_obj.approx_2()
# print('Arkin 2-approx solution', t_approx_len)


m = 5
n = 5
num_stitches = 5
for i in range(10):
    pattern = util.random_pattern(m, n, num_stitches)
    print('Current graph:')
    for v in pattern:
        print(v, pattern[v])

    # DPLL work
    dpll_obj = dpll.DPLL(pattern)
    dpll_obj.make_graph()
    num_vertices = len(dpll_obj.pattern)
    min_val = math.inf
    start_time = time.time()
    for vertex in list(dpll_obj.pattern.keys()):
        start = vertex
        new_val = dpll_obj.dpll(start, start, True, [])
        if new_val < min_val:
            min_val = new_val
    end_time = time.time()
    dpll_time = end_time - start_time

    # Concorde work
    solver = tsp.TSP_Solver(pattern)
    start_time = time.time()
    solver.multi_node_reduction()
    concorde_val = solver.pyconcorde()
    end_time = time.time()
    concorde_time = end_time - start_time

    # TSP work -- redo reduction for fairness
    start_time = time.time()
    solver.multi_node_reduction()
    tsp_val = solver.tsp()
    end_time = time.time()
    tsp_time = end_time - start_time

    # Write to file
    file_write = open('testing_tsp.csv', 'a')
    # Format: m, n, num_stitches, num_vertices, i, time, value
    # file_write.write(str(m) + ',' + str(n) + ',' + str(num_stitches) + ',' + str(num_vertices) + ',' + str(i) + ',' + str(end_time-start_time) + ',' + str(min_val) + '\n')
    # Format: i, label, distance, time
    file_write.write(str(i) + ',dpll,' + str(min_val) + ',' + str(dpll_time) + '\n')
    file_write.write(str(i) + ',conc,' + str(concorde_val) + ',' + str(concorde_time) + '\n')
    file_write.write(str(i) + ',tsp0,' + str(tsp_val) + ',' + str(tsp_time) + '\n')
    file_write.close()
    print('Finished trial', i, 'of', num_stitches, 'stitches')




# # Testing TSP solver
# solver = tsp.TSP_Solver(pattern)
# solver.multi_node_reduction()
# # solver.tsp()
# solver.pyconcorde()
# print('=========================================================')
# solver.tsp()
# # solver.tsp()