import unittest
from src import reader as r
from src import solver
from src import pool as p

class TestSubjectToCriteria(unittest.TestCase):

    def test_subject_to_max_two_cycles(self):
        filename = "tests/datasets/test_max_cycles.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_TWO_CYCLES", "MAX_SIZE"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles[0].donor_patient_nodes), 3)
        
if __name__ == '__main__':
    unittest.main()