import math

class Arkin:
    def __init__(self, pattern):
        self.pattern = pattern
        self.front_edges = []
        self.back_edges = []
        self.t_approx = []

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
                print('ERROR! Caught a self loop in arkin.py')
                print(v1, v2)
                exit(0)
                edge = ((0, 0), (0, 0))
        return edge

    def get_edge_length(self, edge):
        # Assume a edge is a tuple of 2 tuples ((a,b), (c,d))
        x_diff = edge[0][0] - edge[1][0]
        y_diff = edge[0][1] - edge[1][1]
        return math.sqrt(x_diff**2 + y_diff**2)

    """
    For connected instances of G, we can us a polynomial algorithm
    @param: None
    @return dist: optimal tour length (float)
    """
    def b_matchings(self):
        # Idea: we want to ensure that #back edges = #front edges for all vertices
        # "Stage 1. A minimum cost flow problem and its dual are solved (a Hitchcock transposition problem)."
        # "Stage 2. The solutions are processed to obtain optimal 'symmetric' half-integral solutions and 
        #           then to obtain nearly optimal integral solutions."
        # "Stage 3. The nearly optimal solutions are used as input to Pulleyblank's b-matching algorithm."

        # So, we do the min b-matching problem on the back graph with vertex weights b(v) = deg_f(v)
        # Algo in paper: looks like it wants a min b-matching, whereas paper wants max b-matching
        # Then return the size of B edges + size of E edges
        return 0

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
        # Find the components with bfs or dfs on each disconnected edge
        unvisited = list(self.pattern.keys())
        components = []
        while unvisited:
            to_check = unvisited[0]
            # Do DFS traversal
            component = self.dfs(to_check, [], [to_check])
            for node in component:
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
                            edge = self.get_formatted_edge(v1, v2)
                            edge_weight = self.get_edge_length(edge)
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
            queue.append((self.get_edge_length(edge), edge))
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
                        queue.append((self.get_edge_length(e), e))
                    # Pop vertex from v'
                    v_prime.remove(vertex)
            if found_new_vertex:
                mst_edges.append(edge)
        return mst_edges

    """
    Removes redundant back edges
    """
    def remove_consecutive(self):
        print('remove consecutive back edges from T_approx')
    
    """
    Finds a two approximation for the embroidery problem by the Arkin et al. algorithm.
    @param: None
    @return: approximated distance (float)
    """
    def approx_2(self):
        # Find connected components -- constrct G'(V', E')
        g_prime = self.find_components()
        if len(g_prime) == 1:
            return self.b_matchings()
        else:
            # Use Prim's to find the MST
            mst = self.prim(g_prime)
            # Find all front edges from given pattern
            front_edges = []
            self.front_edges = front_edges
            # Remove consecutive back edges
            self.back_edges = mst + mst + front_edges 
            self.t_approx = self.front_edges + self.back_edges
            self.remove_consecutive()
            # Return length of the tour
            # TODO: come back and fill in
            return 5
            """
            length = 0
            for edge in self.t_approx:
                length += len(edge)
            """