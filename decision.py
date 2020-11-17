class Decision:
    # Take in the stitching pattern
    def __init__(self, pattern):
        self.pattern = pattern

    def dpll(self):
        print('TODO: create brute force algorithm')

    def reduce_to_sa(tself):
        print('TODO: convert pattern to CNF formula')

    def simple_sat_solve(self):
        print('TODO: call the raw SimpleSAT solver')
        print('Just clone SimpleSAT and make calls to it')

    def my_sat_solve(self):
        print('TODO: call modified SimpleSAT with clause learning + heuristics')
        print('Fork SimpleSAT and make modifications')

    def industry_sat_solve(self):
        print('TODO: call PythonSAT')

    def tsp_solve(self):
        print('TODO: maybe omit? Use a TSP solver')