def print_pool_donor_nodes(pool):
    for donor_patient_node in pool.donor_patient_nodes:
        donor_id = donor_patient_node.donor
        print(f"Donor ID: {donor_id}")
        for recipient in donor_patient_node.recipient_patients:
            print(f"  Recipient Patient ID: {recipient}")

def print_graph(pool):
        print("Altruists:")
        for altruist in pool.altruists:
            print(f"Altruist ID: {altruist.id}, Age: {altruist.dage}")
            for edge in altruist.out_edges:
                print(f">> Recipient Patient ID: {edge.recipient_patient}, Score: {edge.score}")

        print("\nDonor-Patient Nodes:")
        for donor_patient_node in pool.donor_patient_nodes:
            print(f"Donor ID: {donor_patient_node.donor.id}, Age: {donor_patient_node.donor.dage}, Patient ID: {donor_patient_node.patient.id}")
            for edge in donor_patient_node.out_edges:
                print(f">> Donor Recipient Node: Donor ID: {edge.donor_recipient_node.donor.id}, Patient ID: {edge.donor_recipient_node.patient}, Score: {edge.score}")
            for recipient in donor_patient_node.recipient_patients:
                print(f">> Recipient Patient ID: {recipient.recipient_patient}, Score: {recipient.score}")

def print_cycles(cycles):
    print("\nChecking cycles:")
    count = 0
    for cycle in cycles:  # cycle is a Cycle object
        count += 1
        print("\nCycle:", count)
        for node in cycle.donor_patient_nodes:  # Assuming Cycle has a `.nodes` attribute
            print("Donor:", node.donor.id, "Patient:", node.patient.id)
def print_graph_connectivity(pool):
    print("\nChecking graph connectivity:")
    for node in pool.donor_patient_nodes:
        print(f"\nNode: Donor {node.donor.id}, Patient {node.patient.id}")
        print(f"Number of outgoing edges: {len(node.out_edges)}")
        for edge in node.out_edges:
            print(f"Edge to: Donor {edge.donor_recipient_node.donor.id}, Patient {edge.donor_recipient_node.patient}")
