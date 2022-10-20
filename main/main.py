import uuid
from dataclasses import dataclass


@dataclass
class Transaction:
    order_id: uuid.UUID
    user_id: uuid.UUID
    amount: float
    price: float

    def list(self):
        return [self.order_id, self.user_id, self.amount, self.price]

    def __eq__(self, other):
        return self.order_id == other.order_id and self.user_id == other.user_id


@dataclass
class Bid:
    price: dict
    quantity: dict
    identifier: dict

    def top(self, n: int = 1):
        if n == 1:
            return max(self.price.values())
        return sorted(self.price.values())[:n]

    def add(self, idd, price, quantity):
        order_id = uuid.uuid4()
        if idd not in self.identifier:
            self.identifier[idd] = [order_id]
        else:
            self.identifier[idd].append(order_id)
        self.price[order_id] = price
        self.quantity[order_id] = quantity
        return order_id

    def delete(self, idd, order_id):
        self.identifier[idd].remove(order_id)
        del self.price[order_id]
        del self.quantity[order_id]

    def get_order_id(self, price):
        for order_id, value in self.price.items():
            if price == value:
                return order_id

    def get_idd(self, order_id):
        for idd, value in self.identifier.items():
            if order_id in value:
                return idd


@dataclass
class Ask(Bid):
    def top(self, n: int = 1):
        if n == 1:
            return min(self.price.values())
        return sorted(self.price.values(), reverse=True)[:n]


class OrderBook:
    def __init__(self):
        self._bid: Bid = Bid(price={}, quantity={}, identifier={})
        self._ask: Ask = Ask(price={}, quantity={}, identifier={})
        self.idd = uuid.uuid4()
        self.transactions: list[Transaction] = []

    def _bid_transaction(self, idd, price, amount, ask_order_id):
        self.transactions.append(
            seller := Transaction(
                order_id=ask_order_id,
                user_id=self._ask.get_idd(ask_order_id),
                amount=-amount,
                price=price
            )
        )
        order_id = self._bid.add(idd, price, amount)
        self._bid.delete(idd, order_id)
        self.transactions.append(
            buyer := Transaction(
                order_id=order_id,
                user_id=idd,
                amount=amount,
                price=price
            )
        )
        return seller, buyer

    def add_bid(self, idd, price, quantity):
        if price == self._ask.top():
            ask_order_id = self._ask.get_order_id(price)
            net = self._ask.quantity[ask_order_id] - quantity
            if net <= 0:
                self.delete_ask(idd, ask_order_id)
                self.add_bid(idd, price, abs(net))
                amount = self._ask.quantity[ask_order_id]
            else:
                self._ask.quantity[ask_order_id] = net
                amount = quantity
            return self._bid_transaction(idd, price, amount, ask_order_id)
        elif price > (ask_price := self._ask.top()):
            ask_order_id = self._ask.get_order_id(ask_price)
            net = self._ask.quantity[ask_order_id] - quantity
            if net <= 0:
                self.delete_ask(idd, ask_order_id)
                self.add_bid(idd, price, abs(net))
                amount = self._ask.quantity[ask_order_id]

            return self._bid_transaction(idd, ask_price, quantity)
        else:
            self._bid.add(idd, price, quantity)

    def add_ask(self, idd, price, quantity):
        if price == self._bid.top():
            return self._ask_transaction(idd, price, quantity)
        elif price < (bid_price := self._bid.top()):
            return self._ask_transaction(idd, bid_price, quantity)
        else:
            self._ask.add(idd, price, quantity)

    def delete_bid(self, idd, order_id):
        self._bid.delete(idd, order_id)

    def delete_ask(self, idd, order_id):
        self._ask.delete(idd, order_id)

    def mid_price(self):
        return (self._bid.top() + self._ask.top()) / 2

    def __eq__(self, other):
        return self.idd == other.idd


class Bond:
    def __init__(self, name, coupon, maturity):
        self.name = name
        self.coupon = coupon
        self.maturity = maturity
        self.orders = OrderBook()
        self.idd = uuid.uuid4()

    def price(self):
        self.orders.mid_price()

    def __eq__(self, other):
        return self.idd == other.idd


class Actor:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.idd = uuid.uuid4()

    def __str__(self):
        return f"{self.name} {self.balance}"

    def __eq__(self, other):
        return self.idd == other.idd
