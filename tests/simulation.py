import copy
import random
from pathlib import Path

from coder import Coder
from decoders.decoder import Decoder
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly
from polynomials.binary_poly import BinaryPoly


def print_header(filepath: str = None, file_mode: str = "a"):
    header = f"Errors;Tries;Completed;Failed"
    print(header)

    if filepath is not None:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, file_mode) as f:
            f.write(header + "\n")


def print_results(no_of_errors: int, tries: int, correct_tries: int, incorrect_tries: int, filepath: str = None,
                  file_mode: str = "a"):
    row = f"{no_of_errors};{tries};{correct_tries};{incorrect_tries}"
    print(row)

    if filepath is not None:
        with open(filepath, file_mode) as f:
            f.writelines(row + "\n")


class Simulation:
    M: int = Global.M
    T: int = Global.T

    galois = None
    coder: Coder = None
    decoder: Decoder = None

    def __init__(self, galois, decoder: Decoder):
        self.galois = galois
        self.coder = Coder(galois)
        self.decoder = decoder

        self.text = "Lorem ipsum dolor sit amet."
        self.coded_text = self.coder.code(self.text)[0]

    def test_symbol_errors(self, symbol_errors: dict[int, int]):
        filepath = f"tests\\{type(self.decoder).__name__}\\symbol_tests_results.txt"
        print_header(filepath)

        for (no_of_errors, tries) in symbol_errors.items():
            correct = 0
            for _ in range(tries):
                coded_text_with_errors = self.insert_symbol_error(self.coded_text, no_of_errors)
                decoded_text = self.decoder.decode([coded_text_with_errors])
                correct += 1 if self.text == decoded_text else 0
                print("(in progress...)", end=" ")
                print_results(no_of_errors, tries, correct, tries - correct, filepath=None)

            print_results(no_of_errors, tries, correct, tries - correct, filepath)

    def test_burst_errors(self, burst_errors: dict[int, int]):
        filepath = f"tests\\{type(self.decoder).__name__}\\burst_tests_results.txt"
        print_header(filepath)

        for (burst_len, tries) in burst_errors.items():
            correct = 0

            if burst_len > len(self.coded_text.coefficients):
                burst_len = 6 * (2 ** self.M - 1)
            for i in range(0, tries):
                error_coded = self.insert_burst_error(self.coded_text, burst_len)
                decoded_text = self.decoder.decode([error_coded])
                correct += 1 if self.text == decoded_text else 0
                print("(in progress...)", end=" ")
                print_results(burst_len, tries, correct, tries - correct, filepath=None)

            print_results(burst_len, tries, correct, tries - correct, filepath)

    def insert_symbol_error(self, coded_text: AlphaPoly, error_number: int):
        error_number = min(error_number, len(coded_text.coefficients))
        max_error_value = 2 ** self.M - 2
        max_error_index = len(coded_text.coefficients) - 1
        new_coded_text = copy.deepcopy(coded_text)

        errors_indexes = []
        while len(errors_indexes) < error_number:
            errors_indexes.append(random.randint(0, max_error_index))
            errors_indexes = list(set(errors_indexes))

        for index in errors_indexes:
            error_value = random.randint(1, max_error_value)

            if new_coded_text[index] is None:
                new_coded_text[index] = error_value
            else:
                new_coded_text[index] += error_value

        return new_coded_text

    def insert_burst_error(self, coded_text: AlphaPoly, burst_len: int) -> AlphaPoly:
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
