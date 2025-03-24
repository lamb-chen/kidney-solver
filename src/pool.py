from collections import namedtuple, defaultdict

class AltruistNode(object):
    def __init__(self, id, dage):
        self.id = id
        self.dage = dage
        self.recipient_patients = []
        self.out_edges = []
        self.mip_vars = []
    
    def add_recipient(self, recipient_patient, score):
        self.recipient_patients.append(RecipientWithScore(recipient_patient, score))

    def add_edge(self, target_donor_patient_node, score):
        self.out_edges.append(AltruistEdge(self, target_donor_patient_node, score=score))

class AltruistEdge(object):
    def __init__(self, altruist, target_donor_patient_node, score):
        self.altruist = altruist
        self.target_donor_patient_node = target_donor_patient_node
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
    def __init__(self, donor, patient, is_altruist=False):
        self.donor = donor
        self.patient = patient
        self.recipient_patients = []
        self.out_edges = []
        self.is_altruist = is_altruist

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
    
    def find_backarcs(self):
        backarcs = 0
        for i in range(len(self.donor_patient_nodes)):
            curr_node = self.donor_patient_nodes[i]
            prev_node = self.donor_patient_nodes[i-1]
            for edge in curr_node.out_edges:
                if edge.donor_recipient_node == prev_node:
                    print("\nBackarc pair:")      
                    print("Donor:", curr_node.donor.id, "Patient:", curr_node.patient.id)      
                    print("Donor:", prev_node.donor.id, "Patient:", prev_node.patient.id)                    
                    backarcs += 1
        return backarcs

    def get_cycle_weight(self):
        total_score = 0
        for node in self.donor_patient_nodes:
            total_score += node.score
        return total_score

class Chain(object):
    def __init__(self, altruist_edge, donor_patient_nodes, length, index):
        self.altruist_edge = altruist_edge
        self.donor_patient_nodes = donor_patient_nodes
        self.mip_var = None
        self.length = length
        self.index = index
    
    def find_backarcs(self):
        backarcs = 0
        for i in range(len(self.donor_patient_nodes)):
            curr_node = self.donor_patient_nodes[i]
            prev_node = self.donor_patient_nodes[i-1]
            for edge in curr_node.out_edges:
                if edge.donor_recipient_node == prev_node:
                    print("\nBackarc pair:")      
                    print("Donor:", curr_node.donor.id, "Patient:", curr_node.patient.id)      
                    print("Donor:", prev_node.donor.id, "Patient:", prev_node.patient.id)                    
                    backarcs += 1
        return backarcs
    
    def get_chain_weight(self):
        total_score = 0
        total_score += self.altruist_edge.score
        for node in self.donor_patient_nodes:
            total_score += node.score
        return total_score

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

        for altruist in self.altruists:
            for recipient_with_score in altruist.recipient_patients:
                recipient_patient_id = recipient_with_score.recipient_patient
                score = recipient_with_score.score
                if recipient_patient_id in patient_id_to_nodes:
                    for recipient_node in patient_id_to_nodes[recipient_patient_id]:
                        altruist.add_edge(recipient_node, score)

    def find_cycles(self, max_length):
        cycles = set()
        added = set()
        for start_node in self.donor_patient_nodes:
            path = []
            visited = set()

            def dfs(current_node):
                if len(path) > max_length:
                    return
                # frozenset helps remove duplicates in the tuples
                if path and current_node == start_node and len(path) in range(2, max_length + 1):
                    if frozenset(path) not in added:
                        cycles.add(tuple(path))
                        added.add(frozenset(path))
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
                return
            
            dfs(start_node)
        return cycles

    def create_cycles_and_chain_objects(self, max_length):
        idx = 0

        final_cycles = []
        found_cycles = self.find_cycles(max_length)

        for cycle in found_cycles:
            final_cycles.append(Cycle(list(cycle), len(cycle), idx))
            idx += 1

        final_chains = []
        found_chains = self.find_chains(max_length)

        for chain in found_chains:
            altruist_edge = chain.pop(0)
            final_chains.append(Chain(altruist_edge, chain, len(chain), idx))
            idx += 1

        return final_cycles, final_chains
    
    def find_chains(self, max_length):
        if max_length == 0:
            return []
        
        chains = []
        
        for altruist in self.altruists:
            for edge in altruist.out_edges:
                chain = [edge]  
                
                def dfs(dp_node):
                    if 1 < len(chain) <= max_length:
                        chains.append(chain[:])  # Save a copy of the chain

                    if len(chain) == max_length:
                        return
                    
                    for edge in dp_node.out_edges:
                        next_node = edge.donor_recipient_node
                        chain.append(dp_node)
                        dfs(next_node)
                        chain.pop()  
                
                    return
                
                dp_node = edge.target_donor_patient_node
                dfs(dp_node)
        
        return chains

RecipientWithScore = namedtuple('RecipientWithScore', ['recipient_patient', 'score'])