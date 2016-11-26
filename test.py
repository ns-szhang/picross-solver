import unittest

from picross import Solver


class SolverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = Solver('butterfly.txt')

    def test_evaluate_edge(self):
        """Verify that the solver correctly fills in blocks on the edge"""
        self.assertEqual(self.solver._evaluate([5], "O       "), "OOOOOXXX")
        self.assertEqual(self.solver._evaluate([5], "       O"), "XXXOOOOO")

    def test_evaluate_edge2(self):
        """Verify that the solver intuits when blocks are needed on an edge"""
        self.assertEqual(self.solver._evaluate([5], " O      "), " OOOO XX")
        self.assertEqual(self.solver._evaluate([5], "      O "), "XX OOOO ")

    def test_evaluate_full_row(self):
        """Verify that the solver knows when it has enough information to fill a row"""
        self.assertEqual(self.solver._evaluate([5], "     "), "OOOOO")
        self.assertEqual(self.solver._evaluate([2, 2], "     "), "OOXOO")
        self.assertEqual(self.solver._evaluate([1, 2], "X    "), "XOXOO")

    def test_evaluate_incomplete_row(self):
        self.assertEqual(self.solver._evaluate([4], "     "), " OOO ")

    def test_evaluate_single(self):
        self.assertEqual(self.solver._evaluate([1, 1], "   O   "), "  XOX  ")

    def test_evaluate_unfillable(self):
        """Verify that the solver can determine when a space cannot be filled"""
        self.assertEqual(self.solver._evaluate([2], " X     "), "XX     ")
        self.assertEqual(self.solver._evaluate([2], "     X "), "     XX")

if __name__ == '__main__':
    unittest.main()
