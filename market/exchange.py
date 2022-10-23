from bond import Bond


class BondExchange:
    def __init__(self):
        self._bonds = {}
        self._bond_names = {}

    def add_bond(self, bond: Bond):
        if bond.name in self._bond_names:
            raise ValueError('Bond name is taken')
        self._bond_names[bond.name] = bond.asset_id
        self._bonds[bond.asset_id] = bond
        return bond.asset_id

    def delete_bond(self, asset_id, issuer_id):
        if self._bonds[asset_id].issuer_id == issuer_id:
            self._bonds.pop(asset_id)
        else:
            raise ValueError('Issuer ID does not match')

    def place_order(self, user_id, price, quantity, side, asset_id=None, bond_name=None):
        if asset_id is not None:
            return self._bonds[asset_id].add_order(user_id, price, quantity, side)
        elif bond_name is not None:
            return self._bonds[self._bond_names[bond_name]].add_order(user_id, price, quantity, side)
        else:
            raise ValueError('Either asset_id or bond_name must be specified')

    def cancel_order(self, order_id, asset_id=None, bond_name=None):
        if asset_id is not None:
            self._bonds[asset_id].delete_order(order_id)
        elif bond_name is not None:
            self._bonds[self._bond_names[bond_name]].delete_order(order_id)
        else:
            raise ValueError('Either asset_id or bond_name must be specified')

    def listings(self):
        for bond in self._bonds.values():
            print(bond)

    def show_orderbook(self, asset_id):
        return self._bonds[asset_id].show()
