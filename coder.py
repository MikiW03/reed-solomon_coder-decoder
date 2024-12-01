import galois
from galois import Galois
from polynomials.alpha_poly import AlphaPoly
from global_settings import Global
from polynomials.binary_poly import BinaryPoly

galois = Galois()


def text_to_bit_list(text):
    bit_list = []
    for char in text:
        bits = format(ord(char), '08b')
        bit_list.extend(int(bit) for bit in bits)

    return bit_list


def bit_list_to_text(bit_list):
    chars = []
    for i in range(0, len(bit_list), 8):
        if len(set(bit_list[i:i + 8])) > 1:
            byte = bit_list[i:i + 8]
        else:
            continue
        char = chr(int(''.join(map(str, byte)), 2))
        chars.append(char)

    return ''.join(chars)


def split_list(tab, M):
    if M <= 0:
        raise ValueError("Length has to be greater than 0")

    result = [tab[i:i + M] for i in range(0, len(tab), M)]

    if len(result[-1]) < M:
        result[-1].extend([0] * (M - len(result[-1])))

    return result


def binary_list_to_alphas(binary_lists):
    alphas_list = []
    for binary_list in binary_lists:
        if len(set(binary_list)) > 1 or binary_list[0] != 0:
            alphas_list.append(galois.poly_2_alpha_power(BinaryPoly(binary_list)))
        else:
            alphas_list.append(None)

    return AlphaPoly(alphas_list)


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

    def __init__(self, gallois):
        self.gallois = gallois

    def RS_coder(self, text):
        generative_poly = self.gallois.generate_generative_polynomial()
        n = 2 ** self.M - 1
        k = n - 2 * self.T

        bit_list = text_to_bit_list(text)
        mx = binary_list_to_alphas(split_list(bit_list, self.M))

        list_of_mx = split_poly(mx, k)
        list_of_cx = []

        for mx in list_of_mx:
            multi_m_gen = mx.get_shifted(n - k)
            rx = multi_m_gen % generative_poly

            cx = multi_m_gen + rx
            list_of_cx.append(cx)

            # for i in range(5):
            #     cx_shifted = cx.get_cyclic_shifted(i)
            #     print(f"cx(cyclic shifted {i} times)")
            #     print(f"cx after shift: {cx_shifted}")
            #     print(f"Remainder: {cx_shifted % generative_poly}")
            #     print()
            # print()

        # x = 1
        # y = 59
        # print(AlphaPoly([cx.coefficients[62 - 24 + (25-x)]]) + AlphaPoly([y]))
        # cx.coefficients[62 - 24 + (25-x)] = y
        # cx = AlphaPoly(cx.coefficients)
        #
        # print(cx)
        # print(cx % generative_poly)
        return list_of_cx
