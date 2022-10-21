from orderbook import OrderBook

ob = OrderBook()

ob.add_bid(1, 23, 100)
ob.add_bid(2, 24, 30)
ob.add_bid(3, 10, 20)

ob.add_ask(5, 25, 10)
ob.add_ask(4, 28, 30)
ob.add_ask(8, 30, 50)

print(ob.show())

trans_id, order_id = ob.add_bid(9, 30, 30)

print(ob.show())

trans = ob.show_transactions(trans_id)
trans['value'] = trans['price'] * trans['amount']

print(trans.loc[:, ['user_id', 'value']].groupby('user_id').sum())
