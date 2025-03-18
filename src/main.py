from src import pool as p
from src import reader as r
from src import solver 
from src import printing
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    reader = r.Reader()
    pool = reader.read_json(filename)
    printing.print_pool_donor_nodes(pool)
    printing.print_graph(pool)
    printing.print_graph_connectivity(pool)

    cycles = pool.create_cycle_objects(3)
    printing.print_cycles(cycles)

    g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
    # # g_solver.run_gurobi_cycle_finder(pool.donor_patient_nodes)
    constraint_list = ["MAX_SIZE"]
    optimal_cycles = g_solver.add_contraints(pool.donor_patient_nodes, constraint_list)

    printing.print_optimal_cycles(optimal_cycles)