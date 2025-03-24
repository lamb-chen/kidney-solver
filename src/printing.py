def print_pool_donor_nodes(pool):
    for donor_patient_node in pool.donor_patient_nodes:
        donor_id = donor_patient_node.donor
        print(f"Donor ID: {donor_id}")
        for recipient_with_score in donor_patient_node.recipient_patients:
            print(f"  Recipient Patient ID: {recipient_with_score.recipient_patient}")

def print_graph(pool):
        print("Altruists:")
        for altruist in pool.altruists:
            print(f"Altruist ID: {altruist.id}, Age: {altruist.dage}")
            for edge in altruist.out_edges:
                print(f">> Recipient Patient ID: {edge.target_donor_patient_node.patient.id}, Score: {edge.score}")

        print("\nDonor-Patient Nodes:")
        for donor_patient_node in pool.donor_patient_nodes:
            print(f"Donor ID: {donor_patient_node.donor.id}, Age: {donor_patient_node.donor.dage}, Patient ID: {donor_patient_node.patient.id}")
            for edge in donor_patient_node.out_edges:
                print(f">> Donor Recipient Node: Donor ID: {edge.donor_recipient_node.donor.id}, Patient ID: {edge.donor_recipient_node.patient.id}, Score: {edge.score}")
            for recipient_with_score in donor_patient_node.recipient_patients:
                print(f">> Recipient Patient ID: {recipient_with_score.recipient_patient}, Score: {recipient_with_score.score}")

def print_cycles(cycles):
    print("\nChecking cycles:")
    count = 0
    for cycle in cycles:  
        count += 1
        print("\nCycle:", count)
        for node in cycle.donor_patient_nodes:  
            print("Donor:", node.donor.id, "Patient:", node.patient.id)
        print("cycle: ", cycle.index, "weight: ", cycle.get_cycle_weight())
        print("Num of backarcs: ", cycle.find_backarcs())
        print("\n")

def print_graph_connectivity(pool):
    print("\nChecking graph connectivity:")
    for node in pool.donor_patient_nodes:
        print(f"\nNode: Donor {node.donor.id}, Patient {node.patient.id}")
        print(f"Number of outgoing edges: {len(node.out_edges)}")
        for edge in node.out_edges:
            print(f"Edge to: Donor {edge.donor_recipient_node.donor.id}, Patient {edge.donor_recipient_node.patient}")

def print_optimal_cycles(optimal_cycles):
    for item in optimal_cycles:
        print("Chosen cycle: ", item.index)
        for node in item.donor_patient_nodes:
            print("Donor: ", node.donor.id, "Patient: ", node.patient.id)