import unittest
from src import reader as r
from . import hierarchal
from src import pool as p
from src import analyser

class TestAltruistCycleFinder(unittest.TestCase):

    def test_altruist_cycle_found(self):
        filename = "tests/datasets/test_example.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        self.assertEqual(len(cycles), 9)

    def test_altruist_included(self):
        filename = "tests/datasets/test_example.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = hierarchal.HierarchalOptimiser(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        n_transplants = analyser.get_n_total_transplants(optimal_cycles)
        self.assertEqual(7, n_transplants)
    
    def test_altruist_split_1(self):
        filename = "tests/datasets/test_altruist_split_1.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = hierarchal.HierarchalOptimiser(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles), 1)

    def test_altruist_split_2(self):
        filename = "tests/datasets/test_altruist_split_2.json"
        reader = r.Reader()
        pool = reader.read_json(filename)
        cycles = pool.create_cycles_objects(3)
        g_solver = hierarchal.HierarchalOptimiser(pool=pool, max_length=3, cycles=cycles)
        constraint_list = ["MAX_SIZE"]
        optimal_cycles = g_solver.add_constraints(pool, constraint_list)
        self.assertEqual(len(optimal_cycles), 2)

if __name__ == '__main__':
    unittest.main()