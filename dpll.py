import math

class DPLL:
    def __init__(self, pattern):
        self.pattern = pattern
        self.vertices = pattern.keys()
        self.front_edges = {}
        self.back_edges = {}

    def get_formatted_edge(self, v1, v2):
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
                print('ERROR! Caught a self loop in dpll.py')
                edge = ((0, 0), (0, 0))
        return edge

    def get_edge_length(self, edge):
        # Assume a edge is a tuple of 2 tuples ((a,b), (c,d))
        x_diff = edge[0][0] - edge[1][0]
        y_diff = edge[0][1] - edge[1][1]
        return math.sqrt(x_diff**2 + y_diff**2)

    def make_graph(self):
        # Generate list of front edges by going through the given pattern
        for vertex in self.vertices:
            adj_list = self.pattern[vertex]
            for adj in adj_list:
                edge = self.get_formatted_edge(vertex, adj)
                if edge not in self.front_edges:
                    self.front_edges[edge] = self.get_edge_length(edge)

        # Create all back edges by creating a complete graph
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 != v2:
                    edge = self.get_formatted_edge(v1, v2)
                    if edge not in self.back_edges:
                        self.back_edges[edge] = self.get_edge_length(edge)

    """
    Brute force DPLL algorithm for embroidery problem.
    @param start_vertex: where the cycle started (identifier)
    @param front: whether we're on front or back of fabric (boolean)
    @return: minimum value alternating tour (float)
    """
    def dpll(self, start_vertex, front, taken_so_far):
        # Base case: we've completed a tour!
        # Base case: we're stuck -- there are no edges to take on front side and not a valid tour
        # Recurse: try either the front or back edges, whatever is appropriate
            # Track sum so far in the return statements
        print('DPLL algo TODO')