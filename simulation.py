from coder import Coder
from decoder import Decoder
from galois import Galois
import copy
import random 

class Simulation():
    galois = Galois()
    galois.generate_generative_polynomial()
    coder = Coder(galois)
    decoder = Decoder(galois)

    def start_simulation(this):
        text = "Lorem ipsum dolor sit amet."
        coded_text = this.coder.code(text)

        print(f"Rodzaj błędu | Liczba | Poprawne | Niepoprawne | Poprawne Zle")

        # 1 - 5 error rand
        for err in range(0, 6):
            correct = 0
            number = 5

            for i in range(0, number):
                error_coded = this.insert_error(coded_text, err)
                decoded_text = this.decoder.decode(error_coded)
                correct += 1 if text == decoded_text else 0
            
            print(f" {err} w l. miej.|   {number}    |    {correct}     |     {number - correct}       |      0      ")

    
    def insert_error(this, coded_text, error_number):
        max_error_value = 2 ** this.galois.M - 2
        max_error_index = len(coded_text[0].coefficients) - 1
        new_coded_text = copy.deepcopy(coded_text)

        for i in range(0, error_number):
            error_index = random.randint(0, max_error_index)
            error_value = random.randint(2, max_error_value)

            new_coded_text[0][error_index] = error_value
        
        return new_coded_text

    def insert_burst_error(this, coded_text, error_number, burst_len):
        max_error_value = 2 ** this.galois.M - 2
        max_error_index = len(coded_text[0].coefficients) - burst_len - 1
        new_coded_text = copy.deepcopy(coded_text)

        for i in range(0, error_number):
            error_start_index = random.randint(0, max_error_index)
            for j in range(0, burst_len):
                error_value = random.randint(2, max_error_value)
                if random.randint(0 ,1) == 0:
                    error_index = error_start_index + j

                    new_coded_text[0][error_index] = error_value
        
        return new_coded_text
        
