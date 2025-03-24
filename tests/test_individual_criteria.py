import unittest
from src import reader as r
from src import solver
from src import pool as p


class TestIndividualCriteria(unittest.TestCase):

    def test_max_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 3)

    def test_max_two_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_TWO_CYCLES"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 2)

    def test_max_backarcs(self):
        optimal_cycle_donor_ids = ["0", "1", "2"]

        filename = "tests/datasets/test_max_backarcs.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_BACKARCS"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        for cycle in optimal_cycles:
            for node in cycle.donor_patient_nodes:
                self.assertIn(node.donor.id, optimal_cycle_donor_ids)

    def test_max_backarcs_from_two_cycle(self):
        optimal_cycle_donor_ids = ["0", "1", "3"]
        filename = "tests/datasets/test_max_backarcs_2.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_BACKARCS"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        for cycle in optimal_cycles:
            for node in cycle.donor_patient_nodes:
                self.assertIn(node.donor.id, optimal_cycle_donor_ids)

    def test_min_three_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE", "MIN_THREE_CYCLES"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 2)
        
if __name__ == '__main__':
    unittest.main()