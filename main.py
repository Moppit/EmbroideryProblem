import importlib
import math
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')
arkin = importlib.import_module('arkin')

# Generate a random instance of a stitching pattern
# create a window
m = 4
n = 3

pattern = util.random_pattern(m, n)
# Test case
# pattern = {
#     (2, 2): [(1, 1)],
#     (1, 1): [(2, 2)],
#     (1, 0): [(3, 3), (0, 0), (0, 1)],
#     (3, 3): [(1, 0)],
#     (0, 0): [(0, 1), (1, 0)],
#     (0, 1): [(0, 0), (1, 0)]
# }
util.visual(m, n, pattern)

# TODO: write some known test cases so you can verify whether it's working or not!
# dpll_obj = dpll.DPLL(pattern)
# dpll_obj.make_graph()
# print(dpll_obj.pattern)
# print('---------------------')
# print(dpll_obj.front_edges)
# print('---------------------')
# print(dpll_obj.back_edges)
# print('---------------------')


# Grab some random first item -- if cycle exists, shouldn't matter where we start
"""
min_val = math.inf
if len(pattern) == 0:
    min_val = 0
for vertex in list(dpll_obj.pattern.keys()):
    start = vertex
    new_val = dpll_obj.dpll(start, start, True, [])
    if new_val < min_val:
        min_val = new_val
print(min_val)
"""
# Testing DPLL
dpll_obj = dpll.DPLL(pattern)
dpll_obj.make_graph()
min_val = math.inf
for vertex in list(dpll_obj.pattern.keys()):
    start = vertex
    new_val = dpll_obj.dpll(start, start, True, [])
    if new_val < min_val:
        min_val = new_val
print('DPLL solution:', min_val)

# Testing Arkin
approx2_obj = arkin.Arkin(pattern)
t_approx_len = approx2_obj.approx_2()
print('Arkin 2-approx solution', t_approx_len)