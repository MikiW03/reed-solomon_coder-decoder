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
        raise ValueError("Długość fragmentu musi być większa od zera.")

    result = [tab[i:i + M] for i in range(0, len(tab), M)]

    if len(result[-1]) < M:
        result[-1].extend([0] * (M - len(result[-1])))

    return result


def int_to_polynomial(n):
    poly = [0] * (n + 1)
    poly[0] = 1

    return AlphaPoly(poly)


def binary_lists_to_decimal_list(binary_lists):
    decimal_list = []
    for binary_list in binary_lists:
        decimal_value = 0
        for bit in binary_list:
            decimal_value = (decimal_value << 1) | bit
        decimal_list.append(decimal_value)

    return AlphaPoly(decimal_list)


class Coder:
    M = Global.M
    T = Global.T

    def __init__(self, gallois):
        self.gallois = gallois

    def RS_coder(self, text):
        generative_poly = self.gallois.generate_generative_polynomial()
        n = 2 ** self.M - 1
        k = n - 2 * self.T

        xnk = int_to_polynomial(n - k)
        bit_list = text_to_bit_list(text)
        mx = binary_lists_to_decimal_list(split_list(bit_list, self.M))

        print(f"Xnk: {xnk}")
        print(f"Mx: {mx}")

        multi_m_gen = mx * xnk
        rx = multi_m_gen % generative_poly

        print(f"m * gen: {multi_m_gen}")
        print(f"rx: {rx}\n")

        cx = multi_m_gen + rx

        print(f"Tekst: {text}")
        print(f"Generative poly: {generative_poly}")
        print(f"Lista bitowa: {bit_list}")
        print(f"cx: {cx}")

        print(f"mod: {cx % generative_poly}")
