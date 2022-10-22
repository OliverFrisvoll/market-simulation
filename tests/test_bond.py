import unittest

from datetime import datetime
from bond import Bond


class TestBond(unittest.TestCase):
    def test_par_value(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.par_value, 100)

    def test_maturity(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.maturity, datetime(2019, 12, 31))

    def test_coupon_rate(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.coupon_rate, 0.05)

    def test_coupon_frequency(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.coupon_frequency, 2)

    def test_issuer_id(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.issuer_id, 1)

    def test_yield_to_maturity(self):
        bond = Bond(100, datetime(2019, 12, 31), 0.05, 2, 1)
        self.assertEqual(bond.yield_to_maturity(), 0)




if __name__ == '__main__':
    unittest.main()
