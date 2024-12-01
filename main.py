from decoder import Decoder
from coder import Coder, galois
from galois import Galois

if __name__ == '__main__':
    gallois = Galois()
    coder = Coder(gallois)
    decoder = Decoder(gallois)

    text = "sdadsaa"

    coded_text = coder.RS_coder(text)[0]
    decoded_text = decoder.decode(coded_text)
    print(decoded_text)
