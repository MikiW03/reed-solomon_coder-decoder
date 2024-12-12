from typing import Literal

from alpha import Alpha
from global_settings import Global
from polynomials.binary_poly import BinaryPoly
from polynomials.poly import Poly


class AlphaPoly(Poly):
    M: int = Global.M
    T: int = Global.T

    coefficients: list[int | None] = None
    alphas: list[Alpha] = None
    galois = None

    def __init__(self, coefficients: list[int | None]):
        from galois import Galois
        self.galois = Galois()
        self.coefficients = coefficients
        self.alphas = [Alpha(x) for x in self.coefficients]

    def __str__(self):
        poly = self.alphas
        if len(poly) == 0:
            return "None"

        return f"[{', '.join([str(alpha) for alpha in self.alphas])}]"

    def __repr__(self):
        return f"AlphaPoly({self.coefficients})"

    def __setitem__(self, key: int, value: int):
        new_value = None if value is None else value % (2 ** self.M - 1)

        self.coefficients[key] = new_value
        self.alphas[key] = Alpha(new_value)

    def __getitem__(self, index: int):
        return self.coefficients[index]

    def get_trimmed(self):
        coefficients_copy = self.coefficients[:]
        while len(coefficients_copy) > 1 and coefficients_copy[0] is None:
            coefficients_copy.pop(0)
        return AlphaPoly(coefficients_copy)

    def get_filled(self, desired_no_of_bits: int):
        filled_coefficients = ([None] * (desired_no_of_bits - len(self.coefficients))) + self.coefficients
        return AlphaPoly(filled_coefficients)

    def __add__(self, other):
        max_len = max(len(self.alphas), len(other.alphas))
        poly1 = self.get_filled(max_len).alphas
        poly2 = other.get_filled(max_len).alphas

        alpha_poly = [x + y for (x, y) in zip(poly1, poly2)]
        alpha_poly_coefficients = list(map(lambda x: x.power, alpha_poly))

        return AlphaPoly(alpha_poly_coefficients)

    def division_with_remainder(self, p1, p2):
        poly1 = p1.get_trimmed().coefficients
        poly2 = p2.get_trimmed().coefficients

        if not any(poly2):
            raise ValueError("Divisor cannot be zero polynomial")

        remainder = poly1[:]
        result = []

        iteration = 0
        max_len = len(poly1) - len(poly2)

        while iteration <= max_len:
            if remainder[iteration] is None or poly2[0] is None:
                result.append(None)
                iteration += 1
                continue
            else:
                result.append(remainder[iteration] - poly2[0])

            sub_poly = []
            if result[iteration] is None:
                pass
            elif result[iteration] == 0:
                sub_poly = poly2
            else:
                for i in poly2:
                    if i is None:
                        sub_poly.append(None)
                    elif i == 0:
                        sub_poly.append(result[iteration])
                    else:
                        alfa1 = result[iteration]
                        alfa2 = i

                        value = self.galois.alpha_powers[alfa1] * self.galois.alpha_powers[alfa2]
                        sub_poly.append(self.galois.poly_2_alpha_power(value))

            for i in range(0, len(sub_poly)):
                if remainder[iteration + i] is None:
                    remainder[iteration + i] = sub_poly[i]
                elif remainder[iteration + i] == sub_poly[i]:
                    remainder[iteration + i] = None
                else:
                    alfa1 = remainder[i + iteration]
                    alfa2 = sub_poly[i]

                    value = self.galois.alpha_powers[alfa1] if alfa2 is None else self.galois.alpha_powers[alfa1] + \
                                                                                  self.galois.alpha_powers[alfa2]
                    remainder[iteration + i] = self.galois.poly_2_alpha_power(value)
            iteration += 1
        result = [(x + (2 ** self.M - 1)) if (x is not None and x < 0) else x for x in result]

        return AlphaPoly(result), AlphaPoly(remainder)

    def __truediv__(self, other):
        result, _ = self.division_with_remainder(self, other)
        return result

    def __mod__(self, other):
        _, remainder = self.division_with_remainder(self, other)
        return remainder.get_trimmed()

    def __mul__(self, other):
        poly1 = self.coefficients
        poly2 = other.coefficients

        result = [None] * (len(poly1) + len(poly2) - 1)

        for i in range(len(poly1)):
            if poly1[i] is None:
                continue
            for j in range(len(poly2)):
                if poly2[j] is None:
                    continue
                result[i + j] = \
                    (AlphaPoly([result[i + j]]) + AlphaPoly(
                        [((poly1[i] + poly2[j]) % (2 ** self.M - 1))])).coefficients[0]

        return AlphaPoly(result)

    def get_cyclic_shifted(self, no_of_positions: int, direction: Literal['left', 'right'] = "left"):
        n = len(self.coefficients)
        shifted_coefficients = self.coefficients[:]

        no_of_positions = no_of_positions % n

        if direction == "left":
            shifted_coefficients = shifted_coefficients[no_of_positions:] + shifted_coefficients[:no_of_positions]
        elif direction == "right":
            shifted_coefficients = shifted_coefficients[-no_of_positions:] + shifted_coefficients[:-no_of_positions]
        else:
            raise ValueError("Direction must be 'left' or 'right'")

        return AlphaPoly(shifted_coefficients)

    def get_shifted(self, no_of_positions: int):
        temp: list[int | None] = [None] * no_of_positions

        copy = AlphaPoly(self.coefficients)
        copy *= AlphaPoly([0] + temp)

        return copy

    def get_hamming_weight(self):
        return len(list(filter(lambda x: x is not None, self.coefficients)))

    def to_binary_poly(self):
        binary_list = []

        for alpha in self.coefficients:
            if alpha is None:
                binary_list.extend([0, 0, 0, 0, 0, 0])
            else:
                binary_list.extend(self.galois.alpha_powers[alpha].get_filled(6).coefficients)

        return BinaryPoly(binary_list)

    def replace_x_and_count(self, x: Alpha):
        result = Alpha()
        for (i, alpha) in enumerate(self.alphas):
            result += alpha * (x ** (len(self.coefficients) - i - 1))

        return result
