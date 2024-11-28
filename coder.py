from alpha import Alpha
from polynomials.alpha_poly import AlphaPoly
from global_settings import Global


def text_to_bit_list(text):
    bit_list = []
    for char in text:
        bits = format(ord(char), '08b')
        bit_list.extend(int(bit) for bit in bits)

    return bit_list


def bit_list_to_text(bit_list):
    chars = []
    for i in range(0, len(bit_list), 8):
        byte = bit_list[i:i + 8]
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


def binary_lists_to_decimal_list(binary_lists):
    decimal_list = []
    for binary_list in binary_lists:
        decimal_value = 0
        for bit in binary_list:
            decimal_value = (decimal_value << 1) | bit
        decimal_list.append(decimal_value)

    return AlphaPoly(decimal_list)


def split_poly(poly, size_of_parts):
    fill_value = None
    lst = poly.coefficients

    result = [AlphaPoly(lst[i:i + size_of_parts]) for i in range(0, len(lst), size_of_parts)]
    if len(result[-1]) < size_of_parts:
        result[-1] *= AlphaPoly([1] + [fill_value] * (size_of_parts - len(result[-1])))
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
        mx = binary_lists_to_decimal_list(split_list(bit_list, self.M))

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

        return list_of_cx
