import uuid

from orderbook import OrderBook


class Asset:
    def __init__(self):
        self._orderbook = OrderBook()
        self._asset_id = uuid.uuid4()

    @property
    def asset_id(self):
        return self._asset_id

    def price(self):
        return self._orderbook.price()

    def add_order(self, user_id, price: float, quantity: int, side: str):
        side = side.lower()
        if side == 'bid':
            return self._orderbook.add_bid(user_id, price, quantity)
        elif side == 'ask':
            return self._orderbook.add_ask(user_id, price, quantity)
        else:
            raise ValueError('side must be either bid or ask')

    def delete_order(self, order_id):
        self._orderbook.delete_bid(order_id)
        self._orderbook.delete_ask(order_id)

    def show(self, n: int = 5):
        return self._orderbook.show(n)

    def show_transactions(self, transaction_id):
        return self._orderbook.show_transactions(transaction_id)

    def show_orders(self, order_id):
        return self._orderbook.show_orders(order_id)
