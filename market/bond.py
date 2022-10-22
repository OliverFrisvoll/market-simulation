import numpy as np

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

    @staticmethod
    def _calculate_ytm(maturity: datetime, price: float, cr: float, par_value: int = 1000, coupon_frequency: int = 1):
        """
        Calculates the yield to maturity of a bond given the maturity date, price, coupon rate, par value and coupon frequency.

        :param maturity: datetime - date of maturity
        :param price: float - Price of the bond
        :param cr: float - Coupon rate
        :param par_value: int - Par value of the bond
        :param coupon_frequency: int - Coupon frequency
        :return: float - Yield to maturity
        """

        from scipy import optimize

        coupon = (cr / coupon_frequency) * par_value
        if (years := (maturity - datetime.now()).days / 365) < 0:
            raise ValueError("Maturity date must be in the future")

        T = np.floor(years * coupon_frequency)
        t = years * coupon_frequency - T

        def f(r):
            return coupon / np.power(1 + r, t) + \
                   (coupon / r - coupon / (r * np.power(1 + r, T))) / np.power(1 + r, t) + \
                   par_value / np.power(1 + r, T + t) - \
                   price

        return optimize.newton(f, 0.01)

    def ytm(self):
        if self.price() is None:
            return None
        return self._calculate_ytm(self.maturity, self.price(), self.coupon_rate, self.par_value, self.coupon_frequency)
