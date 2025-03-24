from gurobipy import *
import criteria

class GurobiSolver(object):
    def __init__(self, pool, max_length, cycles, chains):
        self.model = Model()
        self.pool = pool
        self.cycles = cycles
        self.chains = chains
        # self.chains = pool.find_chains()

    def add_vars_to_patients_and_donors(self, donor_patient_nodes, mip_var):
        for node in donor_patient_nodes:
            node.patient.mip_vars.append(mip_var) 
            node.donor.mip_vars.append(mip_var) 
    
    # def add_vars_to_altruists(self, altruists, mip_var):


    def _items_in_optimal_solution(self, items):
            return [item for item in items if item.mip_var.X > 0.5]
    
    def choose_constraints(self, constraint_list, cycles):
        final_constraints = []
        for constraint in constraint_list:
            if constraint == "MAX_TWO_CYCLES":
                final_constraints.append([cycle.mip_var * criteria.MaxTwoCycles().cycle_val(cycle) for cycle in cycles])
            elif constraint == "MAX_SIZE":
                final_constraints.append([cycle.mip_var * criteria.MaxSize().cycle_val(cycle) for cycle in cycles])
            elif constraint == "MAX_BACKARCS":
                final_constraints.append([cycle.mip_var * criteria.MaxBackarcs().cycle_val(cycle) for cycle in cycles])
            elif constraint == "MIN_THREE_CYCLES":
                final_constraints.append([cycle.mip_var * criteria.MinThreeCycles().cycle_val(cycle) for cycle in cycles])
            elif constraint == "MAX_WEIGHT":
                final_constraints.append([cycle.mip_var * criteria.MaxOverallWeight().cycle_val(cycle) for cycle in cycles])
        return final_constraints


        
    def add_constraints(self, pool, constraint_list):

        for cycle in self.cycles:
            cycle.mip_var = self.model.addVar(vtype=GRB.BINARY, name='cycle' + str(cycle.index))
        for chain in self.chains:
            chain.mip_var = self.model.addVar(vtype=GRB.BINARY, name='chain' + str(chain.index))
        for altruist in pool.altruists:
            altruist.mip_var = self.model.addVar(vtype=GRB.BINARY, name='altruist' + str(altruist.id))
            altruist.mip_vars.append(altruist.mip_var)
        self.model.update()

        for cycle in self.cycles:
            self.add_vars_to_patients_and_donors(cycle.donor_patient_nodes, cycle.mip_var)
            
        for node in pool.donor_patient_nodes:
            self.model.addConstr(quicksum(node.patient.mip_vars) <= 1)
            self.model.addConstr(quicksum(node.donor.mip_vars) <= 1)

        self.model.ModelSense = GRB.MAXIMIZE 
        self.model.update()

        final_constraints = self.choose_constraints(constraint_list, self.cycles)
        for i in range(len(final_constraints)):
            print(final_constraints, "FINAL CONSTS")
            if constraint_list[i] == "MIN_THREE_CYCLES":
                self.model.setObjectiveN(-quicksum(final_constraints[i]), index=i, weight=1.0, priority=i, name=f"Objective_{i}")        
            else:
                self.model.setObjectiveN(quicksum(final_constraints[i]), index=i, weight=1.0, priority=i, name=f"Objective_{i}")        
                
        # maximum size cycle i.e. max number of transplants
        # self.model.setObjectiveN(quicksum([cycle.mip_var * criteria.MaxSize().cycle_val(cycle) for cycle in self.cycles]), index=2, weight=1.0, priority=2)        
        # self.model.setObjectiveN(quicksum([cycle.mip_var * criteria.MaxBackarcs().cycle_val(cycle) for cycle in self.cycles]), index=3, weight=1.0, priority=3)        
        # self.model.setObjectiveN(quicksum([cycle.mip_var * criteria.MinThreeCyles().cycle_val(cycle) for cycle in self.cycles]), index=4, weight=-1.0, priority=4)     
        self.model.optimize()
        optimal_cycles = self._items_in_optimal_solution(self.cycles)
        # for var in self.model.getVars():
        #     print(f"{var.varName}: {var.x}")
        return optimal_cycles

    def run_gurobi_cycle_finder(self, donor_patient_nodes):
        edges = []
        for node in donor_patient_nodes:
            u = (node.donor.id, node.patient.id)
            for e in node.out_edges:
                target_node = e.donor_recipient_node
                v = (target_node.donor.id, int(target_node.patient.id))
                edges.append((u, v))

        var_edges = self.model.addVars(edges, vtype=GRB.BINARY, name="edge")
        
        for u, v in edges:
            # Make sure the reverse edge exists
            if (v, u) in edges:
                self.model.addConstr(var_edges[u, v] == var_edges[v, u], name=f"{u}_{v}_two_cycle")

        self.model.setObjective(quicksum(var_edges[u, v] for u, v in edges if (v, u) in edges), GRB.MAXIMIZE)
        self.model.optimize()

        seen = set()
        two_cycles_list = []

        # Finding 2-cycles
        for u, v in edges:
            if (u, v) in edges and (v, u) in edges:
                # > 0.5 means edge has been selected
                # check both to and back have been selected                
                if var_edges[u, v].X > 0.5 and var_edges[v, u].X > 0.5:
                    curr_set = frozenset((u, v))
                    if curr_set not in seen:
                        seen.add(curr_set)
                        two_cycles_list.append((u, v))  

        three_cycles = []
        for u, v in edges:
            for w in donor_patient_nodes:
                w_id = (w.donor.id, w.patient.id)
                if (v, w_id) in edges and (w_id, u) in edges:
                    three_cycles.append((u, v, w_id))

        for (u, v, w) in three_cycles:
            self.model.addConstr(var_edges[u, v] + var_edges[v, w] + var_edges[w, u] == 3, name=f"{u}_{v}_{w}_three_cycle")

        self.model.setObjective(
            quicksum(var_edges[u, v] + var_edges[v, w] + var_edges[w, u] for (u, v, w) in three_cycles) / 3,
            GRB.MAXIMIZE
        )
        
        self.model.optimize()

        seen = set()
        three_cycles_list = []

        # Finding 3-cycles
        for (u, v, w) in three_cycles:
            curr_set = frozenset((u, v, w))
            if curr_set not in seen:
                seen.add(curr_set)
                if var_edges[u, v].X > 0.5 and var_edges[v, w].X > 0.5 and var_edges[w, u].X > 0.5:
                    three_cycles_list.append((u, v, w)) 

        return two_cycles_list, three_cycles_list
