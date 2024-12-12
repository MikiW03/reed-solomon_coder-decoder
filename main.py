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
        1: 100,
        2: 100,
        3: 100,
        4: 100,
        5: 100,
        6: 100,
        7: 100
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
        60: 100,
        62: 100,
        64: 100,
        66: 100,
        68: 100,
        70: 100,
        72: 100,
        74: 100,
        76: 100,
        78: 100,
        80: 100,
        82: 100,
        84: 100,
        86: 100,
        88: 100,
        90: 100,
        92: 100,
        94: 100,
        96: 100,
        98: 100,
        100: 100,
        200: 100,
        300: 100,
        1000: 100
    }

    simpleDecoderSim = Simulation(galois, simpleDecoder)
    simpleDecoderSim.test_symbol_errors(symbol_errors)
    simpleDecoderSim.test_burst_errors(burst_errors)

    # fullDecoderSim = Simulation(galois, fullDecoder)
    # fullDecoderSim.test_symbol_errors(symbol_errors)
    # fullDecoderSim.test_burst_errors(burst_errors)
