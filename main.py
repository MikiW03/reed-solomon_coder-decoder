from decoders.full_decoder import FullDecoder
from decoders.simple_decoder import SimpleDecoder
from galois import Galois
from tests.simulation import Simulation

if __name__ == '__main__':
    galois = Galois()
    galois.generate_generative_polynomial()

    simpleDecoder = SimpleDecoder(galois)
    fullDecoder = FullDecoder(galois)

    symbol_errors = {
        # no_of_errors: tries
        1: 500,
        2: 500,
        3: 500,
        4: 500,
        5: 500
    }

    burst_errors = {
        # burst_length: tries
        1: 100,
        2: 100,
        3: 100,
        6: 100,
        8: 100,
        12: 100,
        15: 100,
        25: 100,
        35: 100,
        45: 100,
        50: 100,
        55: 100,
        60: 500,
        62: 500,
        64: 500,
        66: 500,
        68: 500,
        70: 500,
        72: 500,
        74: 500,
        76: 500,
        78: 500,
        80: 500,
        82: 500,
        84: 500,
        86: 500,
        88: 500,
        90: 500,
        92: 500,
        94: 500,
        96: 500,
        98: 500,
        100: 500,
        200: 500,
        300: 500,
        1000: 500
    }

    simpleDecoderSim = Simulation(galois, simpleDecoder)
    simpleDecoderSim.test_symbol_errors(symbol_errors)
    simpleDecoderSim.test_burst_errors(burst_errors)

    fullDecoderSim = Simulation(galois, fullDecoder)
    fullDecoderSim.test_symbol_errors(symbol_errors)
    fullDecoderSim.test_burst_errors(burst_errors)
