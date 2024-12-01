from decoder import Decoder
from coder import Coder
from galois import Galois

if __name__ == '__main__':
    galois = Galois()
    galois.generate_generative_polynomial()

    coder = Coder(galois)
    decoder = Decoder(galois)

    text = "Lorem ipsum dolor sit amet."
    coded_text = coder.code(text)
    decoded_text = decoder.decode(coded_text)

    print(decoded_text)
    print(f"{'Decoded succesfully' if text == decoded_text else 'Decoded with errors'}")
