from global_settings import Global
from polynomials.alpha_poly import AlphaPoly
from polynomials.binary_poly import BinaryPoly


class Galois:
    M: int = Global.M
    T: int = Global.T

    alpha_powers: list[BinaryPoly] = None
    generative_poly: AlphaPoly = None

    def __init__(self):
        self.alpha_powers = self.generate_alpha_powers()

    def poly_2_alpha_power(self, poly: BinaryPoly):
        if poly == BinaryPoly([0, 0, 0, 0, 0, 0]):
            return None
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

    def binary_poly_to_alpha_poly(self, binary_poly: BinaryPoly) -> AlphaPoly:
        alphas_list = []
        for i in range(0, len(binary_poly.coefficients), 6):
            alphas_list.append(self.poly_2_alpha_power(BinaryPoly(binary_poly.coefficients[i:i + 6])))

        return AlphaPoly(alphas_list)
