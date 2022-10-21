from datetime import datetime

from securities import Asset


class Bond(Asset):
    def __init__(self, par_value, maturity, coupon_rate, coupon_frequency, issuer_id):
        self._par_value = par_value
        self._maturity = maturity
        self._coupon_rate = coupon_rate
        self._coupon_frequency = coupon_frequency
        self._issuer_id = issuer_id
        super().__init__()

    @property
    def par_value(self):
        return self._par_value

    @property
    def maturity(self):
        return self._maturity

    @property
    def coupon_rate(self):
        return self._coupon_rate

    @property
    def coupon_frequency(self):
        return self._coupon_frequency

    @property
    def issuer_id(self):
        return self._issuer_id

    def yield_to_maturity(self):
        price = self.price()
        if price == 0:
            return 0
