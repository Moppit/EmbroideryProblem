# EmbroideryProblem

The Embroidery Problem is an NP-Hard optimization problem that seeks to optimize thread usage while embroidering a given pattern denoted by a Euclidean graph G. A valid embroidery of a pattern is described as a closed tour with alternating front and back edges, each with an associated weight (which, due to the Euclidean integration, is equivalent to the distance between vertices). More details about this problem can be found by the original paper describing it by Arkin *et al*: https://www.researchgate.net/publication/220991070_The_Embroidery_Problem.

Solvers included in this repository:
- DPLL Algorithm
- TSP reduction + solvers
- Arkin 2-approximation algorithm

## Getting Started

### Dependencies
Before running any code, install both PyConcorde and the Python `tsp` package.

For PyConcorde, run the following commands. For more installation details: https://github.com/jvkersch/pyconcorde/blob/master/README.md
```
> git clone https://github.com/jvkersch/pyconcorde
> cd pyconcorde
> pip install -e .
```

For the Python `tsp` package:
```
> pip install tsp
```

### Starter Code
To try out each solver, `main.py` contains some starter code. Run 
```
> python main.py
```
to see the results of running a single (small) embroidery instances through the DPLL solver, the PyConcorde TSP solver, the Python tsp package solver, and the Arkin *et al.* approximation algorithm.

## DPLL Algorithm
This algorithm is implemented in `dpll.py`. The primary function where the DPLL backtracking logic resides is `dpll()`. 

Usage:
```python
# Create a random embroidery pattern using util.py
m = 3
n = 4
num_stitches = 4
pattern = util.random_pattern(m, n, num_stitches)

# Create a dpll solver and generate front and back edges
dpll_solver = dpll.DPLL(pattern)
dpll_solver.make_graph()

# Run the solver on every vertex -- optimal result is the minimum value
dpll_val = math.inf
for vertex in pattern:
    start = vertex
    new_val = dpll_solver.dpll(start, start, True, [])
    if new_val < dpll_val:
        dpll_val = new_val
print('Result:', dpll_val)
```

## TSP Reduction + Solvers
All TSP solver-related code resides in `tsp_solver.py`. There are three major components: the reduction, using PyConcorde, and using the Python `tsp` package. To use the solver, you first have to reduce the given pattern to TSP, and then you can run either the PyConcorde or tsp package version.

### Reduction
The theoretical reduction to TSP is implemented by the function `symmetric_reduction()`. However, the practical version (and the one that is used by both the PyConcorde and tsp package solvers) is written under `multi_node_reduction()`. The difference between the two is minimal: the multi-node version just ensures that no vertices are repeated in the TSP tour.

Usage:
```python
# Create a random embroidery pattern using util.py
m = 3
n = 4
num_stitches = 4
pattern = util.random_pattern(m, n, num_stitches)

# Create a tsp solver and run the reduction
tsp_solver = tsp.TSP_Solver(pattern)
tsp_solver.multi_node_reduction()
```

### PyConcorde
PyConcorde is a Python wrapper around the University of Waterloo's renowned Concorde TSP solver, which is known to be the best TSP solver to date. This wrapper was written by Joris Vankerschaver and can be found here: https://github.com/jvkersch/pyconcorde.

To apply PyConcorde to the reduced embroidery instances, simply run `tour_length = tsp_solver.pyconcorde()`.

### `tsp` Package
The `tsp` Python package is a branch-and-cut linear programming TSP solver written by Saito Tsutomu. It can be found here: https://pypi.org/project/tsp/.

To apply this solver to the reduced embroidery instances, simply run `tour_length = tsp_solver.tsp()`.

## Arkin 2-Approx
The code for Arkin *et al.*'s 2-approximation for the embroidery problem resides in `arkin.py`. Note: this implementation isn't entirely faithful to the one described by Arkin *et al.* -- Anstee's b-matching algorithm was replaced by a simple 2-approximation for connected instances, and the multi-component instances do not have the minimized Euler tour implementation (we simply return the length of 2|MST| + 2|E|, as described in the paper). 

Usage:
```python
# Create a random embroidery pattern using util.py
m = 3
n = 4
num_stitches = 4
pattern = util.random_pattern(m, n, num_stitches)

# Create an Arkin solver
arkin_solver = arkin.Arkin(pattern)
approx = arkin_solver.approx_2()
print('Result:', approx)
```