from polynomials.alpha_poly import AlphaPoly
from global_settings import Global
from polynomials.binary_poly import BinaryPoly


def binary_list_to_alphas(galois, binary_lists):
    alphas_list = []
    for binary_list in binary_lists:
        if len(set(binary_list)) > 1 or binary_list[0] != 0:
            alphas_list.append(galois.poly_2_alpha_power(BinaryPoly(binary_list)))
        else:
            alphas_list.append(None)

    return AlphaPoly(alphas_list)


def text_to_bit_list(text):
    bit_list = []
    for char in text:
        bits = format(ord(char), '08b')
        bit_list.extend(int(bit) for bit in bits)

    return bit_list


def split_list(tab, M):
    if M <= 0:
        raise ValueError("Length has to be greater than 0")

    result = [tab[i:i + M] for i in range(0, len(tab), M)]

    if len(result[-1]) < M:
        result[-1].extend([0] * (M - len(result[-1])))

    return result


def split_poly(poly, size_of_parts):
    fill_value = None
    lst = poly.coefficients

    result = [AlphaPoly(lst[i:i + size_of_parts]) for i in range(0, len(lst), size_of_parts)]
    if len(result[-1]) < size_of_parts:
        result[-1] *= AlphaPoly([0] + [fill_value] * (size_of_parts - len(result[-1])))
    return result


class Coder:
    M = Global.M
    T = Global.T
    galois = None

    def __init__(self, galois):
        self.galois = galois

    def code(self, text):
        generative_poly = self.galois.generative_poly
        n = 2 ** self.M - 1
        k = n - 2 * self.T

        bit_list = text_to_bit_list(text)
        mx = binary_list_to_alphas(self.galois, split_list(bit_list, self.M))

        list_of_mx = split_poly(mx, k)
        list_of_cx = []

        for mx in list_of_mx:
            multi_m_gen = mx.get_shifted(n - k)
            rx = multi_m_gen % generative_poly

            cx = multi_m_gen + rx
            list_of_cx.append(cx)

        return list_of_cx
