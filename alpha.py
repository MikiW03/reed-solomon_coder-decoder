from polynomials.binary_poly import BinaryPoly
from global_settings import Global


class Alpha:
    M = Global.M
    T = Global.T

    def __init__(self, power=None):
        from galois import Galois
        self.galois = Galois()
        self.power = power
        self.poly_representation = BinaryPoly([0]) if self.power is None else self.galois.alpha_powers[power]

    def __repr__(self):
        return f"Alpha({self.power})"

    def __str__(self):
        if self.power is None:
            return "0"
        return f"a^{self.power}"

    def __eq__(self, other):
        return self.power == other.power

    def get_inverse(self):
        if self.power == 0:
            return Alpha(0)
        return Alpha(2 ** self.M - 1 - self.power)

    def __add__(self, other):
        alpha1_poly = self.poly_representation
        alpha2_poly = other.poly_representation

        result = alpha1_poly + alpha2_poly
        if result == BinaryPoly([0]):
            return Alpha()

        return Alpha(self.galois.poly_2_alpha_power(result))

    def __mul__(self, other):
        if self.power is None or other.power is None:
            return Alpha()

        return Alpha((self.power + other.power) % (2 ** self.M - 1))

    def __truediv__(self, other):
        return self * other.get_inverse()
