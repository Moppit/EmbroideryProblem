import random
import numpy as np

"""
Generates a random instance of the embroidery problem.
Inputs:
    m: number rows in Euclidean plane
    n: number columns in Euclidean plane
    density: (defaults = 0.5) determines the ratio of stitches to non-stitched portions
Outputs: Euclidean graph
"""
def random_pattern(m, n, density=0.5):
    print('hello')
    # Create a Euclidean graph in m x n plane
    # There are at most m*n vertices, so there are at most a complete graph of front stitches
    num_front_stitches = int((m*n)*(m*n-1)/2)
    graph = [[None for _ in range(n)] for _ in range(m)]
    print(graph)
    """
    for i in range(num_front_stitches):
        num = random.random()
        if num < density:
            # Generate two stitching endpoints
            start_row, start_col = (np.random.choice(range(n)), np.random.choice(range(m)))
            end_row, end_col = (np.random.choice(range(n)), np.random.choice(range(m)))

    TODO: Continue here! Figure out how to best structure your graph
    """

# TODO: add a benchmarking utility! Would be nice to have consistent format here