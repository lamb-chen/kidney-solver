import unittest
from src import reader as r
from src import solver
from src import pool as p

class TestCycleFinder(unittest.TestCase):

    def test_cycle_finder(self):
        filename = "tests/datasets/test_cycle_count_before.json"
        reader = r.Reader()
        pool_before = reader.read_json(filename)
        before_cycles, _ = pool_before.create_cycles_and_chain_objects(3)
        before_n_cycles = len(before_cycles)

        filename = "tests/datasets/test_cycle_count_after.json"
        pool_after = reader.read_json(filename)
        after_cycles, _ = pool_after.create_cycles_and_chain_objects(3)
        after_n_cycles = len(after_cycles)
        self.assertEqual(before_n_cycles + 1, after_n_cycles)

    def test_cycle_finder_with_gurobi(self):
        filename = "tests/datasets/test_cycle_count_before.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles, chains = pool.create_cycles_and_chain_objects(3)
        g_solver = solver.GurobiSolver(pool=pool, max_length=3, cycles=cycles, chains=chains)
        two_cycles_list, three_cycles_list = g_solver.run_gurobi_cycle_finder(pool.donor_patient_nodes)
        total_cycle_count = len(two_cycles_list) + len(three_cycles_list)
        self.assertEqual(total_cycle_count, len(cycles))

if __name__ == '__main__':
    unittest.main()