class TSP_Solver:
    def __init__(self, pattern):
        self.pattern = pattern
        self.graph = None

    def make_graph(self):
        print('Make into a graph that the pyconcorde solver also likes! That way you can just feed this right into it')
        
    def solve_tsp_simple(self):
        print('solve graph with handwritten TSP solver')

    def solve_tsp_improved(self):
        print('solve graph with handwritten TSP solver (with cutting planes)')

    def pyconcorde(self):
        print('call the pyconcorde package? Figure out how to import it and run')
        print('may want to add instructions for installing and running for ease of grading')