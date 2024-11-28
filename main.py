from coder import Coder
from galois import Galois

if __name__ == '__main__':
    gallois = Galois()
    coder = Coder(gallois)

    text = "AB"
    coded_text = coder.RS_coder(text)
    print(coded_text)
