import unittest

from datetime import datetime
from orderbook import OrderBook


class TestOrderbook(unittest.TestCase):

    def test_add_bid(self):
        ob = OrderBook()

        # Added bid order
        logg, order_id = ob.add_bid(1, 23, 100)
        self.assertEqual(len(logg), 0)
        self.assertTrue(order_id is not None)

        # Added ask order
        logg, order_id = ob.add_ask(2, 26, 100)
        self.assertEqual(len(logg), 0)
        self.assertTrue(order_id is not None)

        # Bid was fulfilled
        logg, order_id = ob.add_bid(3, 28, 40)
        self.assertEqual(len(logg), 1)
        self.assertTrue(order_id is None)

        trans = ob.show_transactions(logg)
        self.assertEqual(len(trans), 2)
        self.assertEqual(trans.loc[:, 'price'].iloc[0], 26)
        self.assertEqual(trans.loc[:, 'amount'].sum(), 0)
        self.assertEqual(trans.loc[:, 'amount'].iloc[0], -40)
        self.assertEqual(trans.loc[:, 'amount'].iloc[1], 40)

        # Ask was fulfilled
        logg, order_id = ob.add_ask(4, 22, 30)
        self.assertEqual(len(logg), 1)
        self.assertTrue(order_id is None)

        trans = ob.show_transactions(logg)
        self.assertEqual(len(trans), 2)
        self.assertEqual(trans.loc[:, 'price'].iloc[0], 23)
        self.assertEqual(trans.loc[:, 'amount'].sum(), 0)
        self.assertEqual(trans.loc[:, 'amount'].iloc[0], -30)
        self.assertEqual(trans.loc[:, 'amount'].iloc[1], 30)

        # Bid was partially fulfilled
        logg, order_id = ob.add_bid(4, 28, 75)
        self.assertEqual(len(logg), 1)
        self.assertTrue(order_id is not None)

        trans = ob.show_transactions(logg)
        self.assertEqual(len(trans), 2)
        self.assertEqual(trans.loc[:, 'price'].iloc[0], 26)
        self.assertEqual(trans.loc[:, 'amount'].sum(), 0)
        self.assertEqual(trans.loc[:, 'amount'].iloc[0], -60)
        self.assertEqual(trans.loc[:, 'amount'].iloc[1], 60)

        # Ask was partially fulfilled
        logg, order_id = ob.add_ask(4, 22, 50)
        self.assertEqual(trans.loc[:, 'price'].iloc[0], 26)
        self.assertEqual(trans.loc[:, 'amount'].iloc[0], -60)
        self.assertEqual(trans.loc[:, 'amount'].iloc[1], 60)

    def test_show(self):
        ob = OrderBook()

        ob.add_bid(1, 23, 100)
        ob.add_bid(2, 24, 30)
        ob.add_bid(3, 10, 20)
        ob.add_ask(5, 25, 10)
        ob.add_ask(4, 28, 30)
        ob.add_ask(8, 30, 50)
        self.assertEqual(ob.show(3).loc[:, 'price'].iloc[0], 30)
        self.assertEqual(ob.show(3).loc[:, 'price'].iloc[1], 28)
        self.assertEqual(ob.show(3).loc[:, 'price'].iloc[2], 25)

    def test_mid_price(self):
        ob = OrderBook()
        self.assertEqual(ob.price(), 0)
        ob.add_ask(5, 25, 10)
        ob.add_bid(2, 24, 30)
        self.assertEqual(ob.price(), 24.5)


if __name__ == '__main__':
    unittest.main()
