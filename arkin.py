import math
import time
import importlib
util = importlib.import_module('util')

class Arkin:
    def __init__(self, pattern):
        self.pattern = pattern
        self.front_edges = []
        self.back_edges = []
        self.t_approx = []

    """
    Finds a connected component within the graph.
    @param vertex: current node we are evaluating
    @return component: list of vertices that were part of this component (list)
    """
    def dfs(self, vertex, component_so_far, visited):
        # Grab all neighbors of this vertex
        component_so_far.append(vertex)
        adj = [node for node in self.pattern[vertex] if node not in visited]
        for v in adj:
            component_so_far = self.dfs(v, component_so_far, visited + [v])
        return component_so_far

    """
    Builds G', which is the graph containing all connected components as vertices, and E' which is a complete graph
    @param: None
    @return: constructed graph G'(V', E')
    """
    def find_components(self):
        # Find the components with dfs on each disconnected edge
        unvisited = list(self.pattern.keys())
        components = []
        while unvisited:
            to_check = unvisited[0]
            # Do DFS traversal
            component = self.dfs(to_check, [], [to_check])
            for node in component:
                if node in unvisited:
                    unvisited.remove(node)
            components.append(component)

        # Create G'
        # Store each of the the components as vertices
        g_prime = {}
        for comp in components:
            comp.sort()
            g_prime[tuple(comp)] = []
        # Create a complete graph on all of those nodes
        for node_1 in g_prime:
            for node_2 in g_prime:
                if node_1 != node_2:
                    # Now create an edge between them. Make sure they're not the same
                    min_edge_weight = math.inf
                    min_edge = None
                    for v1 in node_1:
                        for v2 in node_2:
                            edge = util.get_formatted_edge(v1, v2)
                            edge_weight = util.get_edge_length(edge)
                            if edge_weight < min_edge_weight:
                                min_edge = edge
                                min_edge_weight = edge_weight
                    g_prime[node_1].append(min_edge)
        return g_prime

    """
    Returns the minimum spanning tree of G'
    @param: G' (graph)
    @return: MST of G' (graph)
    """
    def prim(self, g_prime):
        mst_edges = []
        # Get list of vertices in V' and init queue
        v_prime = list(g_prime.keys())
        queue = []
        # Choose a starting vertex and add all of its edges to the queue.
        start = v_prime.pop(0)
        for edge in g_prime[start]:
            queue.append((util.get_edge_length(edge), edge))
        # Pop items off the queue -- if they add something to the tree, add to MST
        while queue:
            queue.sort()
            to_add = queue.pop(0)
            edge_weight = to_add[0]
            edge = to_add[1]
            end_pt_1 = edge[0]
            end_pt_2 = edge[1]
            # Check if one of the endpoints is still a vertex in the graph
            found_new_vertex = False
            for vertex in v_prime:
                if end_pt_1 in vertex or end_pt_2 in vertex:
                    found_new_vertex = True
                    # Add all edges from the new vertex
                    for e in g_prime[vertex]:
                        queue.append((util.get_edge_length(e), e))
                    # Pop vertex from v'
                    v_prime.remove(vertex)
            if found_new_vertex:
                mst_edges.append(edge)
        return mst_edges
    
    """
    Finds a two approximation for the embroidery problem by the Arkin et al. algorithm.
    Note: Arkin et al cite Anstee's b-matching algorithm for connected instances, however, this
          implementation uses a 2-approximation for connected components as well
    @param: None
    @return: approximated distance (float)
    """
    def approx_2(self):
        # Find connected components -- constrct G'(V', E')
        g_prime = self.find_components()
        if len(g_prime) == 1:
            # 2 approximation -- same distance as front edges
            already_counted = []
            total_len = 0
            for v1 in self.pattern:
                for v2 in self.pattern[v1]:
                    edge = util.get_formatted_edge(v1, v2)
                    if edge not in already_counted:
                        already_counted.append(edge)
                        total_len += util.get_edge_length(edge)
            return total_len*2
        else:
            # Use Prim's to find the MST
            mst = self.prim(g_prime)
            # Find all front edges from given pattern
            for vertex in self.pattern:
                adj_list = self.pattern[vertex]
                for adj in adj_list:
                    edge = util.get_formatted_edge(vertex, adj)
                    if edge not in self.front_edges:
                        self.front_edges.append(edge)
            # Remove consecutive back edges
            self.back_edges = mst + mst + self.front_edges 
            self.t_approx = self.front_edges + self.back_edges
            # Return length of the tour
            total_len = 0
            for edge in self.t_approx:
                total_len += util.get_edge_length(edge)
            return total_len