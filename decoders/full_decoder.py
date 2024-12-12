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
        pass
