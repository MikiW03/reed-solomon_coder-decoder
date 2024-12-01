from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


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


def fix_error(message: AlphaPoly, generative_poly, T):
    if message % generative_poly == AlphaPoly([None]):
        return message

    for i in range(len(message)):
        sx = message % generative_poly
        if sx.get_hamming_weight() <= T:
            message += sx
            message = message.get_cyclic_shifted(i, "left")
            return message

        message = message.get_cyclic_shifted(1, "right")

    return message


class Decoder:
    M = Global.M
    T = Global.T
    galois = None

    def __init__(self, galois):
        self.galois = galois

    def decode(self, message):
        message_in_bits = []
        for message_fragment in message:
            message_fragment = fix_error(message_fragment, self.galois.generative_poly, self.T)
            msg = message_fragment.coefficients
            data = [AlphaPoly(msg[:((2 ** self.M - 1) - self.T * 2)]), AlphaPoly(msg[2 ** self.M - self.T * 2:])]

            bit_list = [self.galois.alpha_powers[x].get_filled(6).coefficients if x is not None else [0] * 6 for x in
                        data[0].coefficients]
            for x in bit_list:
                message_in_bits += x

        text = bit_list_to_text(message_in_bits)

        return text
