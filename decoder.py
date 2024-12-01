import coder
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


class Decoder:
    M = Global.M
    T = Global.T

    def __init__(self, gallois):
        self.gallois = gallois

    def decode(self, message):
        gen = self.gallois.generate_generative_polynomial()
        msg = message.coefficients
        data = [AlphaPoly(msg[:((2 ** self.M - 1) - self.T * 2)]), AlphaPoly(msg[2 ** self.M - self.T * 2:])]

        if message % gen == AlphaPoly([None]):
            bit_list = [self.gallois.alpha_powers[x].get_filled(6).coefficients if x is not None else [0] * 6 for x in
                        data[0].coefficients]
            message_in_bits = []
            for x in bit_list:
                message_in_bits += x

            text = coder.bit_list_to_text(message_in_bits)

            return text
