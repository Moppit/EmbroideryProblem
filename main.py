import importlib
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')

# Generate a random instance of a stitching pattern
# create a window
m = 3
n = 5
# util.visual(m, n)
pattern = util.random_pattern(m, n)
dpll_obj = dpll.DPLL(pattern)
dpll_obj.make_graph()

print(dpll_obj.front_edges)
print('---------------------')
print(dpll_obj.back_edges)
print('---------------------')
dpll_obj.dpll('v', True, [])