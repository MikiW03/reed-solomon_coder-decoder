from abc import ABC, abstractmethod

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


class Decoder(ABC):
    @abstractmethod
    def decode(self, message: [AlphaPoly]):
        pass
