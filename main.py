import importlib
util = importlib.import_module('util')
decision = importlib.import_module('decision')
optimization = importlib.import_module('optimization')

# Generate a random instance of a stitching pattern
util.random_pattern(3, 5)
