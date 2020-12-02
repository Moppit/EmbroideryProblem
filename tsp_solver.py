from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path
import tsp
from python_tsp.exact import solve_tsp_dynamic_programming

class TSP_Solver:
    def __init__(self, pattern):
        self.pattern = pattern
        self.graph = None

    def make_adj_matrix(self):
        print('Make into a graph that the pyconcorde solver also likes! That way you can just feed this right into it')
        # Needs a distance matrix!
        # https://hackaday.io/project/158802-improve-tool-path-planning-in-cura/log/147747-using-concorde-tsp-solver
        # Hopefully pyconcorde includes this feature? If not, we'll code it in command line
        # This might be a good TSP solver to modify with cutting planes if they use LP
        # https://pypi.org/project/python-tsp/ -- where you can use pip to install it
        # Here's the github repo
        # Has a good, exact DP solution for solving, which you could use in lieu of 
        
    def solve_tsp_simple(self):
        print('solve graph with handwritten TSP solver')

    def solve_tsp_improved(self):
        print('solve graph with handwritten TSP solver (with cutting planes)')

    def python_tsp(self):
        distance_matrix = np.array([
            [0,  5, 4, 10],
            [5,  0, 8,  5],
            [4,  8, 0,  3],
            [10, 5, 3,  0]
        ])
        permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    
    def tsp_lib(self):
        # Using library here: https://pypi.org/project/tsp/
        # mat = [[0, 1, 1, 999],
        #        [1, 0, 999, 1],
        #        [1, 999, 0, 1],
        #        [999, 1, 1, 0]]  # Symmetric Distance Matrix
        mat = [[0, 5, 4, 999],
               [3, 0, 999, 2],
               [1, 999, 0, 9],
               [999, 8, 7, 0]]  # Asymmetric Distance Matrix
        r = range(len(mat))
        # Dictionary of distance
        dist = {(i, j): mat[i][j] for i in r for j in r}
        print(tsp.tsp(r, dist))

    def pyconcorde(self):
        # fname = get_dataset_path("berlin52")
        print('=======================================================================')
        # print(fname)
        solver = TSPSolver.from_tspfile('t2.tsp')
        solution = solver.solve()
        print(solution.found_tour)
        print(solution.optimal_value)