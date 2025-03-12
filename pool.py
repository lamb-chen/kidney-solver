import json
from collections import namedtuple, defaultdict
import gurobipy as gp
from gurobipy import GRB
import solver 
import printing

class AltruistNode(object):
    def __init__(self, id, dage):
        self.id = id
        self.dage = dage
        self.out_edges = []
        self.mip_vars = []

    def add_edge(self, target_donor_patient_node, score):
        self.out_edges.append(AltruistEdge(target_donor_patient_node, score=score))

class AltruistEdge(object):
    def __init__(self, recipient_patient, score):
        self.recipient_patient = recipient_patient
        self.score = score

class Patient(object):
    def __init__(self, id):
        self.id = id
        self.mip_vars = []

class Donor(object):
    def __init__(self, id, dage):
        self.id = id
        self.dage = dage
        self.mip_vars = []
    
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

class Cycle(object):
    def __init__(self, donor_patient_nodes, length, index):
        self.donor_patient_nodes = donor_patient_nodes
        self.mip_var = None
        self.length = length
        self.index = index

class Chain(object):
    def __init__(self, altruist_edge, dp_nodes, length, index):
        self.altruist_edge = altruist_edge
        self.dp_nodes = dp_nodes
        self.mip_var = None
        self.length = length
        self.index = index


class Pool():
    def __init__(self):
        self.patients = {}
        self.donor_patient_nodes = []
        self.altruists = []

    def add_patient(self, patient):
        self.patients.append(patient)
    
    def add_donor_patient_node(self, donor_patient_node):
        self.donor_patient_nodes.append(donor_patient_node)


    def add_edges_to_nodes(self):
        # id_to_nodes is a dict that stores the patient ids as the key
        # and the corresponding donor_patient_nodes that the patient is
        # related to
        patient_id_to_nodes = defaultdict(list)
        for node in self.donor_patient_nodes:
            patient_id_to_nodes[node.patient.id].append(node)

        # for each donor patient node, the corresponding donor
        # to the recipient patient is found through the id_to_nodes list

        for donor_patient_node in self.donor_patient_nodes:
            for recipient_with_score in donor_patient_node.recipient_patients:
                recipient_patient_id = recipient_with_score.recipient_patient
                score = recipient_with_score.score
                if recipient_patient_id in patient_id_to_nodes:
                    for recipient_node in patient_id_to_nodes[recipient_patient_id]:
                        donor_patient_node.add_edge(recipient_node, score)

    # def return_cycles(self, max_cycle_length):
    #     cycles = []

    #     # removes duplicates from find_cycles function
    #     for dp_node in self.donor_patient_nodes:
    #         curr_cycle = set()
    #         curr_cycle.add(dp_node)
    #         length = max_cycle_length

    #         for out_edge in dp_node.out_edges:
    #             self.find_cycles(dp_node, out_edge.donor_recipient_node, curr_cycle, cycles, length - 1)

    #     return cycles

    def find_cycles(self, max_length):
        cycles = set()
        for start_node in self.donor_patient_nodes:
            path = []
            visited = set()
            def dfs(current_node):
                if len(path) > max_length:
                    return
                # frozenset helps remove duplicates in the tuples
                if path and current_node == start_node and len(path) in range(2, max_length + 1):
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

    def create_cycle_objects(self, max_length):
        final_cycles = []
        found_cycles = self.find_cycles(max_length)
        idx = 0
        for cycle in found_cycles:
            final_cycles.append(Cycle(list(cycle), len(cycle), idx))
            idx += 1
        return final_cycles
    
RecipientWithScore = namedtuple('RecipientWithScore', ['recipient_patient', 'score'])

pool = Pool()

# reading from test.json and creating pool graph
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
                        pool.patients[recipient_patient_id] = Patient(recipient_patient_id)
                        seen_patient_ids.add(recipient_patient_id)

                    score = int(matched_patient["score"])
                    altruist.add_edge(recipient_patient_id, score)
            pool.altruists.append(altruist)
        else:
            donor_obj = Donor(donor_id, dage)
            for source_patient_id in donor["sources"]:
                if source_patient_id not in seen_patient_ids:
                    pool.patients[source_patient_id] = Patient(source_patient_id)
                    seen_patient_ids.add(source_patient_id)
                donor_patient_node = DonorPatientNode(donor_obj, pool.patients[source_patient_id])
                if "matches" in donor:
                    for matched_patient in donor["matches"]:
                            recipient_patient_id = matched_patient["recipient"]

                            if recipient_patient_id not in seen_patient_ids: 
                                pool.patients[recipient_patient_id] = Patient(recipient_patient_id)
                                seen_patient_ids.add(recipient_patient_id)

                            score = int(matched_patient["score"])
                            donor_patient_node.add_recipient(recipient_patient_id, score)
                pool.add_donor_patient_node(donor_patient_node)

                
pool.add_edges_to_nodes()
printing.print_pool_donor_nodes(pool)
printing.print_graph(pool)
printing.print_graph_connectivity(pool)

cycles = pool.create_cycle_objects(3)
printing.print_cycles(cycles)

g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
# g_solver.run_gurobi_cycle_finder(pool.donor_patient_nodes)
g_solver.add_contraints(pool.donor_patient_nodes)
