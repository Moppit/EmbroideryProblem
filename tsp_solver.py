from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path
import tsp
import importlib
util = importlib.import_module('util')
# from python_tsp.exact import solve_tsp_dynamic_programming

class TSP_Solver:
    def __init__(self, pattern):
        self.pattern = pattern
        self.symmetric_graph = None
        self.asymmetric_graph = None

    """
    Reduction 1: to undirected TSP.
    Assigned self.symmetric_graph to a 2D adjacency matrix where 9999 means nodes are not connected 
    @param: None
    @return: None ... TODO: add time taken for reduction
    """
    def symmetric_reduction(self):
        # Create a map for all original nodes in V
        node_map = [node for node in self.pattern]
        gap = len(node_map)

        # Create empty lists for all v in V, v' in V, and alternating gadgets
        reduction = [ [] for _ in range(3*gap)]

        # Add all neighbors to v' nodes and alternating gadget edges
        for i in range(gap, 2*gap):
            # Add all alternating gadget edges (both directions, both fabric sides)
            # V' <-> alternating gadget
            reduction[i].append( (i+gap, 1) )
            reduction[i+gap].append( (i, 1) )
            # V <-> alternating gadget
            reduction[i-gap].append( (i+gap, 1) )
            reduction[i+gap].append( (i-gap, 1) )
            # Add all other vertices if not the corresponding v vertex for v'
            for node in node_map:
                node_idx = node_map.index(node)
                if node_idx != i-gap:
                    dist = util.get_edge_length(node, node_map[i-gap])
                    reduction[i].append( (node_idx+gap, dist) )

        # Add all front edge gadgets
        hashtable = {}
        for v in self.pattern:
            adj = self.pattern[v]
            gadget_made = [[],[]]
            if v in hashtable:
                gadget_made = hashtable[v]
            for node in adj:
                # Make distance half of the original
                distance = util.get_edge_length(v, node)/2
                # If there are values in hash table, check if node matches
                if node in gadget_made[0]:
                    shared_idx = gadget_made[0].index(node)
                    gadget_idx = gadget_made[1][shared_idx]
                    front_origin_idx = node_map.index(v)
                    # Add existing gadget
                    reduction[front_origin_idx].append( (gadget_idx, distance) )
                    reduction[gadget_idx].append( (front_origin_idx, distance) )
                # If not in hash table, will have to add other endpoint in hash table
                else:
                    # Add gadget to reduction
                    new_gadget = len(reduction)
                    reduction.append([])
                    v_idx = node_map.index(v)
                    reduction[new_gadget].append( (v_idx, distance) )
                    reduction[v_idx].append( (new_gadget, distance) )
                    # Add the endpoint in the hashtable
                    if node not in hashtable:
                        hashtable[node] = [[], []]
                    hashtable[node][0].append(v)
                    hashtable[node][1].append(new_gadget)

        # Convert reduction into an adjacency
        self.symmetric_graph = [ [1000 for _ in range(len(reduction))] for _ in range(len(reduction)) ]
        for i in range(len(reduction)):
            self.symmetric_graph[i][i] = 0
            adj = reduction[i]
            for val in adj:
                self.symmetric_graph[i][val[0]] = val[1]

    def asymmetric_reduction(self):
        print('Assymetric reduction')
        # Create adj. matrix (not numpy array... can do conversion within python-tsp call)
        # What does the adj matrix look like?
        # - Self loops = 0
        # - Non-connected nodes = 9999
        # - Symmetric reduction

    """
    Using the python-tsp Python package by Fillipe Goulart.
    Dynamic programming approach to solving TSP exactly.
    """
    def python_tsp(self):
        # TODO: For symmetric, make sure to subtract 2|V| at the end!
        distance_matrix = np.array([
            [0,  5, 4, 10],
            [5,  0, 8,  5],
            [4,  8, 0,  3],
            [10, 5, 3,  0]
        ])
        permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    
    """
    Using the tsp Python package by Saito Tsutomu.
    URL: https://pypi.org/project/tsp/
    Linear programming approach to solving TSP exactly many times, but not guaranteed.
    """
    def tsp(self):
        # TODO: For symmetric, make sure to subtract 2|V| at the end!
        r = range(len(self.symmetric_graph))
        # Dictionary of distance
        dist = {(i, j): self.symmetric_graph[i][j] for i in r for j in r}
        route_length, tour = tsp.tsp(r, dist)
        print(route_length - 2*len(self.pattern))
        print(tour)
        # TODO: deleteme! Print adj matrix
        for row in self.symmetric_graph:
            print([round(n, 2) for n in row])

    """
    Using the PyConcorde by Joris Vankerschaver.
    Python wrapper around Concorde, which is generally regarded as the best TSP solver
        created to this day. Uses branch and cut method (linear programming).
    """
    def pyconcorde(self):
        # TODO: For symmetric, make sure to subtract 2|V| at the end!
        # fname = get_dataset_path("berlin52")
        # TODO: maybe do timing within here, since will have to do some processing
        # and writing to file stuff first
        print('=======================================================================')
        # print(fname)
        solver = TSPSolver.from_tspfile('t2.tsp')
        solution = solver.solve()
        print(solution.found_tour)
        print(solution.optimal_value)