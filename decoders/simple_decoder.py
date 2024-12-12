from decoders.decoder import Decoder, bit_list_to_text, fix_error
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


class SimpleDecoder(Decoder):
    M = Global.M
    T = Global.T
    galois = None

    def __init__(self, galois):
        self.galois = galois

    def decode(self, message: [AlphaPoly]):
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
