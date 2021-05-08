import importlib
import math
import time
util = importlib.import_module('util')
dpll = importlib.import_module('dpll')
arkin = importlib.import_module('arkin')
tsp = importlib.import_module('tsp_solver')

# Environment Specifications
m = 5
n = 5
MAX_STITCHES = 100
NUM_TRIALS = 100
MAX_MEAN_TIME = 10
dpll_run = True
concorde_run = True
tsp_run = True
arkin_run = True

# CSV File
filename_stub = "final_all"
file_write = open(filename_stub + str(time.time()) + ".csv", 'w')
file_write.write("Embroidery Problem Data, time all measured in seconds\n")
file_write.write("# stitches,trial,dpll time,dpll len,concorde time,concorde len,tsp time,tsp len,arkin time,arkin len\n")

mean_file = "final_means"
mean_file_write = open(mean_file + str(time.time()) + ".csv", 'w')
mean_file_write.write("Mean Times From Each Group of 100 Trials\n")
mean_file_write.write("# stitches,dpll time,concorde time,tsp time,arkin time\n")

for num_stitches in range(1, MAX_STITCHES):
    
    # Store all of the values for each calculation to get the mean afterwards
    dpll_times = []
    concorde_times = []
    tsp_times = []
    arkin_times = []

    for trial in range(NUM_TRIALS):

        pattern = util.random_pattern(m, n, num_stitches)

        # 1. DPLL Solver
        if dpll_run:
            dpll_solver = dpll.DPLL(pattern)
            dpll_solver.make_graph()
            dpll_start = time.time()
            dpll_val = math.inf
            if len(pattern) == 0:
                dpll_val = 0
            for vertex in pattern:
                start = vertex
                new_val = dpll_solver.dpll(start, start, True, [])
                if new_val < dpll_val:
                    dpll_val = new_val
            dpll_end = time.time()
        else:
            dpll_start = 1
            dpll_end = 0
            dpll_val = math.inf

        # 2. TSP Reduction
        tsp_solver = tsp.TSP_Solver(pattern)

        # PyConcorde solver
        if concorde_run:
            concorde_start = time.time()
            tsp_solver.multi_node_reduction()
            concorde_val = tsp_solver.pyconcorde()
            concorde_end = time.time()
        else:
            concorde_start = 1
            concorde_end = 0
            concorde_val = math.inf

        # tsp package solver
        if tsp_run:
            tsp_start = time.time()
            tsp_solver.multi_node_reduction()
            tsp_val = tsp_solver.tsp()
            tsp_end = time.time()
        else:
            tsp_start = 1
            tsp_end = 0
            tsp_val = math.inf

        # 3. Arkin
        if arkin_run:
            arkin_start = time.time()
            arkin_approx = arkin.Arkin(pattern)
            arkin_val = arkin_approx.approx_2()
            arkin_end = time.time()
        else:
            arkin_start = 1
            arkin_end = 0
            arkin_val = math.inf

        # Write results
        file_write.write(
            str(num_stitches) + "," + str(trial) + ","
            + str(dpll_end-dpll_start) + "," + str(dpll_val) + "," 
            + str(concorde_end-concorde_start) + "," + str(concorde_val) + "," 
            + str(tsp_end-tsp_start) + "," + str(tsp_val) + "," 
            + str(arkin_end-arkin_start) + "," + str(arkin_val) + "\n")
        dpll_times.append(dpll_end-dpll_start)
        concorde_times.append(concorde_end-concorde_start)
        tsp_times.append(tsp_end-tsp_start)
        arkin_times.append(arkin_end-arkin_start)

    # Write mean values to new spreadsheet
    dpll_mean = sum(dpll_times)/len(dpll_times)
    concorde_mean = sum(concorde_times)/len(concorde_times)
    tsp_mean = sum(tsp_times)/len(tsp_times)
    arkin_mean = sum(arkin_times)/len(arkin_times)

    mean_file_write.write(
        str(num_stitches) + ","
        + str(dpll_mean) + ","
        + str(concorde_mean) + ","
        + str(tsp_mean) + ","
        + str(arkin_mean) + "\n")

    # If mean is greater than target time, stop running those trials
    if dpll_run and dpll_mean > MAX_MEAN_TIME:
        dpll_run = False
    if concorde_run and concorde_mean > MAX_MEAN_TIME:
        concorde_run = False
    if tsp_run and tsp_mean > MAX_MEAN_TIME:
        tsp_run = False    
    if arkin_run and arkin_mean > MAX_MEAN_TIME:
        arkin_run = False

    # Print mean here so I can track progress
    print("Finished num stitches", num_stitches)
    time.sleep(0.1)

file_write.close()
mean_file_write.close()
