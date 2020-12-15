import importlib
import math
import time
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')
arkin = importlib.import_module('arkin')
tsp = importlib.import_module('tsp_solver')

# Generate a random instance of a stitching pattern and display
m = 5
n = 5
num_stitches = 4
pattern = util.random_pattern(m, n, num_stitches)
util.visual(m, n, pattern)

# 1. DPLL Solver
dpll_solver = dpll.DPLL(pattern)
dpll_solver.make_graph()
dpll_start = time.time()
dpll_val = math.inf
if len(pattern) == 0:
    dpll_val = 0
for vertex in pattern:
    start = vertex
    new_val = dpll_solver.dpll(start, start, True, [])
    if new_val < dpll_val:
        dpll_val = new_val
dpll_end = time.time()

# 2. TSP Reduction
tsp_solver = tsp.TSP_Solver(pattern)

# PyConcorde solver
concorde_start = time.time()
tsp_solver.multi_node_reduction()
concorde_val = tsp_solver.pyconcorde()
concorde_end = time.time()

# tsp package solver
tsp_start = time.time()
tsp_solver.multi_node_reduction()
tsp_val = tsp_solver.tsp()
tsp_end = time.time()

# 3. Arkin
arkin_start = time.time()
arkin_approx = arkin.Arkin(pattern)
arkin_val = arkin_approx.approx_2()
arkin_end = time.time()

# Print results
print('-----------------------------------------------')
print('|                   Results                   |')
print('-----------------------------------------------')
print('DPLL solver result:', dpll_val, 'in', dpll_end-dpll_start, 'seconds')
print('PyConcorde TSP solver result:', concorde_val, 'in', concorde_end-concorde_start, 'seconds')
print('tsp package solver result:', tsp_val, 'in', tsp_end-tsp_start, 'seconds')
print('Arkin approximation result:', arkin_val, 'in', arkin_end-arkin_start, 'seconds')
