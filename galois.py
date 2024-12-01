from polynomials.alpha_poly import AlphaPoly
from polynomials.binary_poly import BinaryPoly
from global_settings import Global


class Galois:
    M = Global.M
    T = Global.T

    alpha_powers = None
    generative_poly = None

    def __init__(self):
        self.alpha_powers = self.generate_alpha_powers()

    def poly_2_alpha_power(self, poly):
        return self.alpha_powers.index(poly)

    def generate_alpha_powers(self):
        alpha = BinaryPoly([1, 0])
        powers = [BinaryPoly([1])]
        current = BinaryPoly([1])

        for i in range(1, 2 ** self.M - 1):
            current *= alpha
            powers.append(current)

        return powers

    def generate_generative_polynomial(self):
        generative_poly = AlphaPoly([0, 1])

        for i in range(2, 2 * self.T):
            term = AlphaPoly([0, i])
            generative_poly *= term

        self.generative_poly = generative_poly
