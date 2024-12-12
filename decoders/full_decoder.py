from decoders.decoder import Decoder
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


class FullDecoder(Decoder):
    M = Global.M
    T = Global.T
    galois = None

    def __init__(self, galois):
        self.galois = galois

    def decode(self, message: [AlphaPoly]):
        pass
