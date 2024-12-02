
from coder import Coder
from decoder import Decoder
from global_settings import Global
import copy
import random 

from polynomials.alpha_poly import AlphaPoly
from polynomials.binary_poly import BinaryPoly


class Simulation:
    M = Global.M
    T = Global.T

    galois = None
    coder = None
    decoder = None

    def __init__(self, galois):
        self.galois = galois
        self.coder = Coder(galois)
        self.decoder = Decoder(galois)

    def start_simulation(self, tries: int, burst_errors: list) -> None:
        text = "Lorem ipsum dolor sit amet."
        coded_text = self.coder.code(text)[0]

        print(f"Rodzaj błędu | Liczba | Poprawne | Niepoprawne | Poprawne Zle")

        number = tries
        for burst_len in burst_errors:
            correct = 0

            if burst_len > len(coded_text.coefficients):
                burst_len = 6 * (2 ** self.M - 1)
            for i in range(0, number):
                error_coded = self.insert_burst_error(coded_text, burst_len)
                decoded_text = self.decoder.decode([error_coded])
                correct += 1 if text == decoded_text else 0

            print(
                f" {burst_len} w l. miej.|   {number}    |    {correct}     |     {number - correct}       |      0      ")

    def insert_error(self, coded_text, error_number):
        max_error_value = 2 ** self.galois.M - 2
        max_error_index = len(coded_text[0].coefficients) - 1
        new_coded_text = copy.deepcopy(coded_text)

        for i in range(error_number):
            error_index = random.randint(0, max_error_index)
            error_value = random.randint(0, max_error_value)

            new_coded_text[0][error_index] = error_value

        return new_coded_text

    def insert_burst_error(self, coded_text: AlphaPoly, burst_len) -> AlphaPoly:
        binary_coded_text = coded_text.to_binary_poly().coefficients

        max_starting_index = len(binary_coded_text) - burst_len - 1
        if burst_len >= len(binary_coded_text):
            starting_index = 0
            burst_len = len(binary_coded_text)
        else:
            starting_index = random.randint(0, max_starting_index)

        for i in range(burst_len):
            binary_coded_text[starting_index + i] = 1 - binary_coded_text[starting_index + i]

        return self.galois.binary_poly_to_alpha_poly(BinaryPoly(binary_coded_text))
