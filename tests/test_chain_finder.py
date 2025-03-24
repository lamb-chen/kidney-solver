# import unittest
# from src import reader as r
# from src import solver
# from src import pool as p
# from src import printing

# class TestChainFinder(unittest.TestCase):

#     def test_chain_finder(self):
#         filename = "tests/datasets/test_chain_finder_1.json"
#         reader = r.Reader()
#         pool = reader.read_json(filename)
#         _, chains = pool.create_cycles_and_chain_objects(3)
#         self.assertEqual(len(chains), 4)
    
#     def test_split_chain(self):
#         filename = "tests/datasets/test_chain_finder_2.json"
#         reader = r.Reader()
#         pool = reader.read_json(filename)
#         _, chains = pool.create_cycles_and_chain_objects(3)
#         printing.print_chains(chains)
#         self.assertEqual(len(chains), 2)

#     def test_final_only_picks_one_chain(self):
#         filename = "tests/datasets/test_chain_finder_2.json"
#         reader = r.Reader()
#         pool = reader.read_json(filename)
#         _, chains = pool.create_cycles_and_chain_objects(3)
#         printing.print_chains(chains)
#         self.assertEqual(len(chains), 2)

# if __name__ == '__main__':
#     unittest.main()