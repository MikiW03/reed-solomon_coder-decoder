from alpha import Alpha
from decoders.decoder import Decoder
from galois import Galois
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


class FullDecoder(Decoder):
    M: int = Global.M
    T: int = Global.T
    galois: Galois = None

    def __init__(self, galois: Galois):
        self.galois = galois

    def decode(self, message: list[AlphaPoly]) -> str:
        syndromes = self.calculate_syndromes(message)
        print(syndromes)

        return ""

    def calculate_syndromes(self, message: list[AlphaPoly]) -> list[Alpha]:
        # TODO
        syndromes = []
        for message_fragment in message:
            for i in range(1, 2 * self.T):
                syndrome = message_fragment.replace_x_and_count(Alpha(i))
                syndromes.append(syndrome)

        return syndromes
