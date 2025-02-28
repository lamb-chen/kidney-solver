import json
from collections import namedtuple, defaultdict, deque


class Donor(object):
    def __init__(self, id, dage):
        self.id = id
        self.dage = dage    

class AltruistNode(object):
    def __init__(self, id, dage):
        self.id = id
        self.dage = dage
        self.out_edges = []

    def add_edge(self, target_donor_patient_node, score):
        self.out_edges.append(AltruistEdge(target_donor_patient_node, score=score))

class AltruistEdge(object):
    def __init__(self, recipient_patient, score):
        self.recipient_patient = recipient_patient
        self.score = score

class Patient(object):
    def __init__(self, id):
        self.id = id
    
class DonorPatientNode(object):
    def __init__(self, donor, patient):
        self.donor = donor
        self.patient = patient
        self.recipient_patients = []
        self.out_edges = []

    def add_edge(self, target_donor_patient_node, score):
        self.out_edges.append(DonorPatientEdge(target_donor_patient_node, score=score))

    def add_recipient(self, recipient_patient, score):
        self.recipient_patients.append(RecipientWithScore(recipient_patient, score))

class DonorPatientEdge(object):
    def __init__(self, donor_recipient_node, score):
        self.donor_recipient_node = donor_recipient_node
        self.score = score

class Pool():
    def __init__(self):
        self.patients = []
        self.donor_patient_nodes = []
        self.altruists = []
        self.cycles = []

    def add_patient(self, patient):
        self.patients.append(patient)
    
    def add_donor_patient_node(self, donor_patient_node):
        self.donor_patient_nodes.append(donor_patient_node)

    def add_edges_to_nodes(self):
        id_to_nodes = defaultdict(list)
        for node in self.donor_patient_nodes:
            id_to_nodes[node.patient].append(node)
        for donor_patient_node in self.donor_patient_nodes:
            for recipient_with_score in donor_patient_node.recipient_patients:
                recipient_patient_id = recipient_with_score.recipient_patient
                score = recipient_with_score.score
                if recipient_patient_id in id_to_nodes:
                    for recipient_node in id_to_nodes[recipient_patient_id]:
                        donor_patient_node.add_edge(recipient_node, score)

    def return_cycles(self, max_cycle_length):
        cycles = []
        for dp_node in self.donor_patient_nodes:
            curr_cycle = set()
            curr_cycle.add(dp_node)
            length = max_cycle_length
            for out_edge in dp_node.out_edges:
                self.find_cycles(dp_node, out_edge.donor_recipient_node, curr_cycle, cycles, length - 1)
        return cycles

    def find_cycles(self, max_length):
        cycles = set()
        for start_node in self.donor_patient_nodes:
            print(f"\nStarting search from node: Donor {start_node.donor.id}, Patient {start_node.patient}")

            path = []
            visited = set()

            def dfs(current_node):
                if len(path) > max_length:
                    return
                    
                if path and current_node == start_node and len(path) == max_length:
                    cycles.add(frozenset(path))
                    return
                    
                if current_node in visited:
                    return
                    
                visited.add(current_node)
                path.append(current_node)
                
                for edge in current_node.out_edges:
                    next_node = edge.donor_recipient_node
                    dfs(next_node)
                
                path.pop()
                visited.remove(current_node)
            
            dfs(start_node)
        
        return cycles


def print_pool_donor_nodes(pool):
    for donor_patient_node in pool.donor_patient_nodes:
        donor_id = donor_patient_node.donor.id
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
            print(f"Donor ID: {donor_patient_node.donor.id}, Age: {donor_patient_node.donor.dage}, Patient ID: {donor_patient_node.patient}")
            for edge in donor_patient_node.out_edges:
                print(f">> Donor Recipient Node: Donor ID: {edge.donor_recipient_node.donor.id}, Patient ID: {edge.donor_recipient_node.patient}, Score: {edge.score}")
            for recipient in donor_patient_node.recipient_patients:
                print(f">> Recipient Patient ID: {recipient.recipient_patient}, Score: {recipient.score}")


RecipientWithScore = namedtuple('RecipientWithScore', ['recipient_patient', 'score'])

pool = Pool()
# reading from test.json and creating pool graph
# want to first add all the (d, p) npdes and altruist nodes, along with altruist edges
# cannot yet add the dp edges as do not have all dps!
with open("test.json") as dataset_json:
    json_data = json.load(dataset_json)["data"]
    seen_patient_ids = set()

    for donor_id in json_data:
        donor = json_data[donor_id]
        dage = int(donor["dage"])

        is_altruistic = "altruistic" in json_data[donor_id] and json_data[donor_id]["altruistic"]
        if is_altruistic:
            altruist = AltruistNode(donor_id, dage)
            if "matches" in donor:
                for matched_patient in donor["matches"]:
                    recipient_patient_id = matched_patient["recipient"]

                    if recipient_patient_id not in seen_patient_ids: 
                        pool.patients.append(recipient_patient_id)
                        seen_patient_ids.add(recipient_patient_id)

                    score = int(matched_patient["score"])
                    altruist.add_edge(recipient_patient_id, score)

            pool.altruists.append(altruist)

        else:
            for source_patient_id in donor["sources"]:
                if source_patient_id not in seen_patient_ids:
                    pool.patients.append(source_patient_id)
                    seen_patient_ids.add(source_patient_id)

                donor_patient_node = DonorPatientNode(Donor(donor_id, dage), source_patient_id)
                if "matches" in donor:
                    for matched_patient in donor["matches"]:
                            recipient_patient_id = matched_patient["recipient"]

                            if recipient_patient_id not in seen_patient_ids: 
                                pool.patients.append(recipient_patient_id)
                                seen_patient_ids.add(recipient_patient_id)

                            score = int(matched_patient["score"])
                            donor_patient_node.add_recipient(recipient_patient_id, score)

                pool.add_donor_patient_node(donor_patient_node)
pool.add_edges_to_nodes()
print_pool_donor_nodes(pool)
print_graph(pool)

print("\nChecking graph connectivity:")
for node in pool.donor_patient_nodes:
    print(f"\nNode: Donor {node.donor.id}, Patient {node.patient}")
    print(f"Number of outgoing edges: {len(node.out_edges)}")
    for edge in node.out_edges:
        print(f"Edge to: Donor {edge.donor_recipient_node.donor.id}, Patient {edge.donor_recipient_node.patient}")

cycs = pool.find_cycles(3)
print("\nChecking cycles:")
for pair_frozen in cycs:
    pair = list(pair_frozen)
    print(f"\nPair:(Node: Donor {pair[0].donor.id}, Patient {pair[0].patient}, Node: Donor {pair[1].donor.id}, Patient {pair[1].patient}, Node: Donor {pair[2].donor.id}, Patient {pair[2].patient})")
