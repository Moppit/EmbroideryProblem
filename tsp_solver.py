from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path
import tsp
import importlib
util = importlib.import_module('util')
import math

class TSP_Solver:
    def __init__(self, pattern):
        self.pattern = pattern
        self.symmetric_graph = None
        self.multi_node_graph = None

    """
    Reduction 1: to undirected TSP.
    Assigned self.symmetric_graph to a 2D adjacency matrix where 9999 means nodes are not connected 
    @param: None
    @return: None
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
        self.symmetric_graph = [ [9999 for _ in range(len(reduction))] for _ in range(len(reduction)) ]
        for i in range(len(reduction)):
            self.symmetric_graph[i][i] = 0
            adj = reduction[i]
            for val in adj:
                self.symmetric_graph[i][val[0]] = val[1]

    """
    Reduction 2: Modified to accommodate TSP solvers, which only access each vertex once
    Assigned self.multi_node_graph to a 2D adjacency matrix where 9999 means nodes are not connected 
    @param: None
    @return: None
    """
    def multi_node_reduction(self):
        # Convert given pattern into set of disjoint edges where each node is duplicated
        # so it can only be paired with one of its neighbors
        expand_pattern = []
        for node in self.pattern:
            for neighbor in self.pattern[node]:
                expand_pattern.append( (node, neighbor) )

        # Create a map for all of the duplicated nodes from the original graph
        # Treat every node as its first constituent -- use other node for identification
        node_map = [node for node in expand_pattern]
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
            # (or the same first node)
            for node in node_map:
                node_idx = node_map.index(node)
                # Make sure they don't have the same first node (could also check this by dist != 0)
                if node_idx != i-gap and node[0] != node_map[i-gap][0]:
                    dist = util.get_edge_length(node[0], node_map[i-gap][0])
                    reduction[i].append( (node_idx+gap, dist) )

        # Add all front edge gadgets
        gadget_made = []
        for pair in node_map:
            v1 = pair[0]
            v2 = pair[1]
            # See if we made the gadget already -- if so, skip
            if pair in gadget_made:
                gadget_made.remove(pair)
            # If not, create gadget for both sides
            else:
                # Make distance half of the original
                distance = util.get_edge_length(pair[0], pair[1])/2

                # Add gadget to reduction
                new_gadget = len(reduction)
                reduction.append([])
                pair_fwd_idx = node_map.index(pair)
                pair_backward_idx = node_map.index( (v2, v1) )
                reduction[new_gadget].append( (pair_fwd_idx, distance) )
                reduction[new_gadget].append( (pair_backward_idx, distance) )
                reduction[pair_fwd_idx].append( (new_gadget, distance) )
                reduction[pair_backward_idx].append( (new_gadget, distance) )
                
                # Add inverse to the visited list
                gadget_made.append((v2, v1))

        # Convert reduction into an adjacency
        self.multi_node_graph = [ [9999 for _ in range(len(reduction))] for _ in range(len(reduction)) ]
        for i in range(len(reduction)):
            self.multi_node_graph[i][i] = 0
            adj = reduction[i]
            for val in adj:
                self.multi_node_graph[i][val[0]] = val[1]
    
    """
    Using the tsp Python package by Saito Tsutomu.
    URL: https://pypi.org/project/tsp/
    Linear programming approach to solving TSP with fairly good precision
    """
    def tsp(self):
        # Edge case: check for no stitches
        if len(self.multi_node_graph) == 0:
            return 0

        # Dictionary of distance
        r = range(len(self.multi_node_graph))
        dist = {(i, j): self.multi_node_graph[i][j] for i in r for j in r}
        route_length, tour = tsp.tsp(r, dist)

        # Calculate excess distance -- every duplicate node needs distance
        excess = 0
        for v in self.pattern:
            excess += 2*len(self.pattern[v])
        
        # Return length without excess
        return route_length - excess

    """
    Using the PyConcorde by Joris Vankerschaver.
    Python wrapper around Concorde, which is generally regarded as the best TSP solver
        created to this day. Uses branch and cut method (linear programming).
    """
    def pyconcorde(self):
        # Edge case: check for no stitches
        if len(self.multi_node_graph) == 0:
            return 0
        
        # Create tsp file
        filename = 'embroidery.tsp'
        file_write = open(filename, 'w')
        file_write.write('NAME: Embroidery Reduction\n')
        file_write.write('TYPE: TSP\n')
        file_write.write('COMMENT: Concorde on a reduction from the embroidery problem\n')
        file_write.write('DIMENSION: ' + str(len(self.multi_node_graph)) + '\n')
        file_write.write('EDGE_WEIGHT_TYPE: EXPLICIT\n')
        file_write.write('EDGE_WEIGHT_FORMAT: FULL_MATRIX\n')
        file_write.write('EDGE_WEIGHT_SECTION\n')

        # Go through each row of the matrix, round up value, write to file
        for row in self.multi_node_graph:
            to_add = ''
            for val in row:
                to_add += str(math.ceil(val)) + ' '
            file_write.write(to_add + '\n')
        file_write.write('EOF')
        file_write.close()

        # Solve instances
        solver = TSPSolver.from_tspfile(filename)
        solution = solver.solve()

        # Calculate excess distance -- every duplicate node needs distance
        excess = 0
        for v in self.pattern:
            excess += 2*len(self.pattern[v])

        return solution.optimal_value - excess