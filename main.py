import importlib
import math
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')
arkin = importlib.import_module('arkin')

# Generate a random instance of a stitching pattern
# create a window
m = 3
n = 3

pattern = util.random_pattern(m, n)
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

# Testing Arkin
approx2_obj = arkin.Arkin(pattern)
g_prime = approx2_obj.find_components()
approx2_obj.prim(g_prime)
print(g_prime)