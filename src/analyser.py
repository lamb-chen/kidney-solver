def get_n_total_transplants(optimal_cycles):
    node_count = 0
    for cycle in optimal_cycles:
        for node in cycle.donor_patient_nodes:
            node_count += 1
    return node_count