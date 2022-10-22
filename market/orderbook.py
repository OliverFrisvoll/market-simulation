import uuid
import time
from dataclasses import dataclass
import pandas as pd


@dataclass
class TransactionLogg:
    logg: pd.DataFrame = pd.DataFrame(columns=['transaction_id', 'user_id', 'amount', 'price', 'action', 'time'])

    def transaction(self, transaction_id, user_id, amount, price, action):
        transaction = pd.DataFrame([[transaction_id, user_id, amount, price, action, time.time()]],
                                   columns=self.logg.columns)
        self.logg = pd.concat([self.logg, transaction])

    def fetch_transaction(self, identifier, id_type: str = 'transaction_id'):
        if id_type in ['transaction_id', 'user_id']:
            return self.logg.loc[self.logg[id_type].isin(identifier)]
        return None


@dataclass
class Bid:
    orders = pd.DataFrame(columns=['idd', 'timestamp', 'price', 'quantity'])

    def peek(self, n: int = 5):
        if self.orders.empty:
            return None
        return self.orders.reset_index().loc[:, ['price', 'quantity']].head(n)

    def fetch_order(self, identifier, id_type: str = 'idd'):
        if id_type in ['idd', 'order_id']:
            orders = self.orders.loc[self.orders[id_type].isin(identifier)]
            if orders.empty:
                return None
        return None

    def top(self):
        if self.orders.empty:
            return None
        return self.orders.iloc[0]

    def add(self, idd, price, quantity):
        order_id = uuid.uuid4()

        self.orders = pd.concat(
            [self.orders,
             pd.DataFrame([[idd, time.time(), price, quantity]], columns=self.orders.columns, index=[order_id])])

        self.orders.sort_values(by=['price', 'timestamp'], ascending=[False, True], inplace=True)
        return order_id

    def delete(self, order_id):
        self.orders.drop(order_id, inplace=True)


@dataclass
class Ask(Bid):
    def add(self, idd, price, quantity):
        order_id = uuid.uuid4()

        self.orders = pd.concat(
            [self.orders,
             pd.DataFrame([[idd, time.time(), price, quantity]], columns=self.orders.columns, index=[order_id])])

        self.orders.sort_values(by=['price', 'timestamp'], ascending=[True, True], inplace=True)
        return order_id

    def delete(self, order_id):
        self.orders.drop(order_id, inplace=True)


class OrderBook:
    def __init__(self):
        self._bid: Bid = Bid()
        self._ask: Ask = Ask()
        self._ob_id = uuid.uuid4()
        self._transactions = TransactionLogg()

    @property
    def ob_id(self):
        return self._ob_id

    def transaction(self, bid_id, ask_id, price, quantity):
        transaction_id = uuid.uuid4()
        self._transactions.transaction(transaction_id, ask_id, -quantity, price, "sell")
        self._transactions.transaction(transaction_id, bid_id, quantity, price, "buy")
        return transaction_id

    def add_bid(self, user_id, bid: float, quantity: int):
        transaction_ids = []
        order_id = None
        while quantity > 0:
            top = self._ask.top()
            if top is not None and top['price'] <= bid:
                net = top['quantity'] - quantity
                if net < 0:
                    transaction_ids.append(self.transaction(user_id, top['idd'], top['price'], top['quantity']))
                    self.delete_ask(top.name)
                    quantity = quantity - top['quantity']
                elif net == 0:
                    transaction_ids.append(self.transaction(user_id, top['idd'], top['price'], top['quantity']))
                    quantity = 0
                    self.delete_ask(top.name)
                else:
                    transaction_ids.append(self.transaction(user_id, top['idd'], top['price'], quantity))
                    self._ask.orders.loc[top.name, 'quantity'] = net
                    quantity = 0
            else:
                order_id = self._bid.add(user_id, bid, quantity)
                quantity = 0
        return transaction_ids, order_id

    def add_ask(self, user_id, ask: float, quantity: int):
        transaction_ids = []
        order_id = None
        while quantity > 0:
            top = self._bid.top()
            if top is not None and top['price'] >= ask:
                net = top['quantity'] - quantity
                if net < 0:
                    transaction_ids.append(self.transaction(top['idd'], user_id, top['price'], top['quantity']))
                    self.delete_bid(top.name)
                    quantity = -top['quantity']
                elif net == 0:
                    transaction_ids.append(self.transaction(top['idd'], user_id, top['price'], top['quantity']))
                    quantity = 0
                    self.delete_bid(top.name)
                else:
                    transaction_ids.append(self.transaction(top['idd'], user_id, top['price'], quantity))
                    self._bid.orders.loc[top.name, 'quantity'] = net
                    quantity = 0
            else:
                order_id = self._ask.add(user_id, ask, quantity)
                quantity = 0

        return transaction_ids, order_id

    def delete_bid(self, order_id):
        self._bid.delete(order_id)

    def delete_ask(self, order_id):
        self._ask.delete(order_id)

    def mid_price(self):
        if self._bid.orders.empty or self._ask.orders.empty:
            return 0
        return (self._bid.top()['price'] + self._ask.top()['price']) / 2

    def show_bid(self, n: int = 5):
        return self._bid.peek(n)

    def show_ask(self, n: int = 5):
        return self._ask.peek(n)

    def show(self, n: int = 5):
        mid = pd.DataFrame([[self.mid_price(), "---"]], columns=['price', 'BID/ASK'])
        if self.show_ask() is None or self.show_bid() is None:
            return mid
        ask = self.show_ask(5).iloc[::-1]
        ask['BID/ASK'] = 'ASK'
        bid = self.show_bid(5)
        bid['BID/ASK'] = 'BID'
        return pd.concat([ask, mid, bid]).reset_index().loc[:, ['BID/ASK', 'price', 'quantity']]

    def show_transactions(self, identifier, id_type: str = 'transaction_id'):
        return self._transactions.fetch_transaction(identifier, id_type)

    def show_orders(self, identifier, id_type: str = 'order_id') -> tuple:
        return self._bid.fetch_order(identifier, id_type), self._ask.fetch_order(identifier, id_type)

    def __eq__(self, other):
        return self.ob_id == other.ob_id
