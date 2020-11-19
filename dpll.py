class DPLL:
    def __init__(self, graph):
        self.pattern = pattern
        self.graph = None

    def make_graph(self):
        print('make the pattern DPLL-algo friendly')

    """
    Brute force DPLL algorithm for embroidery problem.
    @param start_vertex: where the cycle started (identifier)
    @param front: whether we're on front or back of fabric (boolean)
    @return: minimum value alternating tour (float)
    """
    def dpll(self, start_vertex, front):
        # Base case: we've completed a tour!
        # Base case: we're stuck -- there are no edges to take on front side and not a valid tour
        # Recurse: try either the front or back edges, whatever is appropriate
            # Track sum so far in the return statements