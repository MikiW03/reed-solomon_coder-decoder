from global_settings import Global
from polynomials.poly import Poly


def binary_vector_division(dividend: list[int], divisor: list[int]):
    len_dividend = len(dividend)
    len_divisor = len(divisor)

    quotient = [0] * (len_dividend - len_divisor + 1)
    remainder = dividend.copy()

    for i in range(len_dividend - len_divisor + 1):
        if remainder[i] == 1:
            quotient[i] = 1
            for j in range(len_divisor):
                remainder[i + j] ^= divisor[j]

    while len(remainder) > 0 and remainder[0] == 0:
        remainder.pop(0)

    return quotient, remainder


class BinaryPoly(Poly):
    M: int = Global.M
    T: int = Global.T
    IRREDUCIBLE_POLY: list[int] = Global.IRREDUCIBLE_POLY

    coefficients: list[int] = None

    def __init__(self, coefficients: list[int]):
        self.coefficients = coefficients

    def __str__(self):
        poly = self.coefficients
        if len(poly) == 0:
            return "0"

        terms = []
        degree = len(poly) - 1

        for i in range(degree, -1, -1):
            if poly[degree - i] == 1:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")

        if len(terms) == 0:
            return "0"
        return " + ".join(terms)

    def __repr__(self):
        return f"BinaryPoly({self.coefficients})"

    def get_value(self):
        num = 0
        for (index, b) in enumerate(reversed(self.coefficients)):
            num += b * (2 ** index)
        return num

    def get_trimmed(self):
        coefficients_copy = self.coefficients[:]
        while len(coefficients_copy) > 1 and coefficients_copy[0] == 0:
            coefficients_copy.pop(0)
        return BinaryPoly(coefficients_copy)

    def get_filled(self, desired_no_of_bits: int):
        coefficients_copy = self.coefficients[:]
        for _ in range(desired_no_of_bits - len(self.coefficients)):
            coefficients_copy = [0] + coefficients_copy
        return BinaryPoly(coefficients_copy)

    def get_inverse(self):
        dividend = self.IRREDUCIBLE_POLY
        divisor = self.coefficients

        if divisor == [0]:
            return None
        elif divisor == [1]:
            return BinaryPoly([1])

        matter = []

        quotient, remainder = binary_vector_division(dividend, divisor)
        matter.append(((6 - len(quotient)) * [0]) + quotient)

        remainders = [remainder]

        while remainder != [1]:
            dividend = divisor
            divisor = remainder
            quotient, remainder = binary_vector_division(dividend, divisor)
            matter.append(((6 - len(quotient)) * [0]) + quotient)
            remainders.append(remainder)

        if len(remainders) > 1:
            matter.append(((6 - len(remainders[-2])) * [0]) + remainders[-2])

        zerob = [0, 0, 0, 0, 0, 0]
        oneb = [0, 0, 0, 0, 0, 1]

        final_val = BinaryPoly(zerob)

        if len(matter) == 1:
            final_val += BinaryPoly(matter[0])

            return final_val
        elif len(matter) == 3:
            final_val += BinaryPoly(matter[0])
            final_val *= BinaryPoly(matter[1])
            final_val += BinaryPoly(oneb)

            return final_val
        elif len(matter) > 3:
            prog_values = []
            final_val += BinaryPoly(matter[0])
            prog_values.append(final_val)
            final_val *= BinaryPoly(matter[1])
            final_val += BinaryPoly(oneb)
            prog_values.append(final_val)

            for you in matter[2:len(matter) - 1]:
                final_val = prog_values[1] * BinaryPoly(you)
                prog_values[0] += final_val
                prog_values[1], prog_values[0] = prog_values[0], prog_values[1]

            return prog_values[1]

    def __truediv__(self, other):
        return None if self is None or other.get_inverse() is None else self * other.get_inverse()

    def __add__(self, other):
        max_len = max(len(self.coefficients), len(other.coefficients))

        coefficients1 = self.get_filled(max_len).coefficients
        coefficients2 = other.get_filled(max_len).coefficients

        result = [(coefficients1[i] if i < len(coefficients1) else 0) ^
                  (coefficients2[i] if i < len(coefficients2) else 0)
                  for i in range(max_len)]
        return BinaryPoly(result)

    def __mul__(self, other):
        result = 0
        a = self.get_value()
        b = other.get_value()
        while b > 0:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 2 ** self.M:
                a ^= BinaryPoly(self.IRREDUCIBLE_POLY).get_value()
            b >>= 1

        return BinaryPoly([int(x) for x in bin(result)[2:]])

    def __mod__(self, other):
        dividend = self.coefficients[:]
        divisor = other.coefficients
        while len(dividend) >= len(divisor):
            if dividend[0] != 0:
                for i in range(len(divisor)):
                    dividend[i] ^= divisor[i]
            dividend.pop(0)
        return BinaryPoly(dividend)
