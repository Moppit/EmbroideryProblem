import math
import importlib
util = importlib.import_module('util')

class DPLL:
    def __init__(self, pattern):
        self.pattern = pattern
        self.vertices = pattern.keys()
        self.front_edges = {}
        self.back_edges = {}

    def make_graph(self):
        # Generate list of front edges by going through the given pattern
        for vertex in self.vertices:
            adj_list = self.pattern[vertex]
            for adj in adj_list:
                edge = util.get_formatted_edge(vertex, adj)
                if edge not in self.front_edges:
                    self.front_edges[edge] = util.get_edge_length(edge)

        # Create all back edges by creating a complete graph
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 != v2:
                    edge = util.get_formatted_edge(v1, v2)
                    if edge not in self.back_edges:
                        self.back_edges[edge] = util.get_edge_length(edge)

    """
    Brute force DPLL algorithm for embroidery problem.
    @param start_vertex: where the cycle started (identifier)
    @param current_vertex: where we are currently (identifier)
    @param front: whether we're on front or back of fabric (boolean)
    @param taken_so_far: front edges we've taken. DO NOT include back edges. (List[identifiers])
    @return: minimum value alternating tour (float)
    """
    def dpll(self, start_vertex, current_vertex, front, taken_so_far):
        # Base case: we've completed a tour! Return so we can find min
        if set(taken_so_far) == set(self.front_edges.keys()) and current_vertex == start_vertex:
            return 0
        # Front stitch
        if front:
            adjacency = self.pattern[current_vertex]
            options = []
            for next_vertex in adjacency:
                edge = util.get_formatted_edge(current_vertex, next_vertex)
                if edge not in taken_so_far:
                    # Recurse: try all non-taken front edges -- return min value
                    options.append(util.get_edge_length(edge) + self.dpll(start_vertex, next_vertex, False, taken_so_far + [edge]))
            # Find minimum, unless we didn't find any, in which case return infinity
            return min(options, default=math.inf)
        # Back stitch
        else:
            # Recurse: try all back edges -- be sure to return the minimum value
            options = []
            for next_vertex in self.vertices:
                if current_vertex != next_vertex:
                    edge = util.get_formatted_edge(current_vertex, next_vertex)
                    options.append(util.get_edge_length(edge) + self.dpll(start_vertex, next_vertex, True, taken_so_far))
            return min(options, default=math.inf)