import unittest
from src import reader as r
from src import solver
from src import pool

class TestCriteriaSolver(unittest.TestCase):

    def test_max_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycle_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE"]
        optimal_cycles = g_solver.add_contraints(pool.donor_patient_nodes, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 3)

    def test_max_two_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycle_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_TWO_CYCLES"]
        optimal_cycles = g_solver.add_contraints(pool.donor_patient_nodes, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 2)
    
    def test_subject_to_max_two_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycle_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_TWO_CYCLES", "MAX_SIZE"]
        optimal_cycles = g_solver.add_contraints(pool.donor_patient_nodes, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 3)

if __name__ == '__main__':
    unittest.main()