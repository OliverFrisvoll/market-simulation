import unittest

from datetime import datetime
from bond import Bond

b = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)


class TestBond(unittest.TestCase):
    def test_par_value(self):
        test_bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(test_bond.par_value, 100)


if __name__ == '__main__':
    unittest.main()
