import pool as p
import reader as r
import hierarchal 
import printing
import sys
import analyser


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
    printing.print_graph(pool)

    cycles = pool.create_cycles_objects(3)
    printing.print_cycles(cycles)
    # printing.print_chains(chains)

    g_solver = hierarchal.HierarchalOptimiser(pool=pool, max_length=3, cycles=cycles)
    # # g_solver.run_gurobi_cycle_finder(pool.donor_patient_nodes)
    constraint_list = ["MAX_TWO_CYCLES", "MAX_SIZE", "MAX_BACKARCS", "MIN_THREE_CYCLES", "MAX_WEIGHT"]
    optimal_cycles = g_solver.add_constraints(pool, constraint_list)
    print(analyser.get_n_total_transplants(optimal_cycles),"\n")
    print(analyser.get_total_weight(optimal_cycles),"\n")
    printing.print_optimal_cycles(optimal_cycles)