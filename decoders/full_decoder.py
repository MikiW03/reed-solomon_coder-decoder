from alpha import Alpha
from decoders.decoder import Decoder
from galois import Galois
from global_settings import Global
from polynomials.alpha_poly import AlphaPoly


def print_list_of_alpha_poly(alpha_poly_list: list[AlphaPoly]) -> list[str]:
    return list(map(lambda x: str(x), alpha_poly_list))


class FullDecoder(Decoder):
    M: int = Global.M
    T: int = Global.T
    galois: Galois = None

    def __init__(self, galois: Galois):
        self.galois = galois

    def decode(self, message: list[AlphaPoly]) -> (str, list[AlphaPoly]):
        syndromes = self.calculate_syndromes(message)
        # print("Syndromes: ", end="")
        # print(print_list_of_alpha_poly(syndromes))

        err_locator = self.find_err_locator(syndromes)
        # print("Error locator polynomial: ", end="")
        # print(print_list_of_alpha_poly(err_locator))

        errors_positions = self.find_errors(err_locator)
        print("Error indexes found: ", end="")
        print(errors_positions)

        error_evaluator = self.find_error_evaluator(syndromes, err_locator)
        # print("Errors evaluator: ", end="")
        # print(print_list_of_alpha_poly(error_evaluator))

        error_magnitudes = self.find_error_magnitude(err_locator, errors_positions, error_evaluator)
        print("\nFound errors magnitudes: ", end="")
        print(print_list_of_alpha_poly(error_magnitudes))

        return "", message

    def calculate_syndromes(self, message: list[AlphaPoly]) -> list[AlphaPoly]:
        syndromes_list = []
        for message_fragment in message:
            syndromes_poly = []
            for i in range(1, 2 * self.T):
                syndrome = message_fragment.replace_x_and_count(Alpha(i))
                syndromes_poly.append(syndrome.power)
            syndromes_list.append(AlphaPoly(syndromes_poly))

        return syndromes_list

    def find_err_locator(self, syndromes_list: list[AlphaPoly]) -> list[AlphaPoly]:
        err_locs = []
        for syndromes in syndromes_list:
            err_loc: list[int | None] = [0]
            old_loc: list[int | None] = [0]

            for i in range(0, len(syndromes)):
                delta = Alpha(syndromes[i])
                for j in range(1, len(err_loc)):
                    delta += Alpha(err_loc[-(j + 1)]) * Alpha(syndromes[i - j])

                old_loc = old_loc + [None]

                if delta != Alpha(None):
                    if len(old_loc) > len(err_loc):
                        new_loc = AlphaPoly(old_loc).scale(delta).coefficients
                        old_loc = AlphaPoly(err_loc).scale(delta.get_inverse()).coefficients

                        err_loc = new_loc

                    err_loc = (AlphaPoly(err_loc) + AlphaPoly(old_loc).scale(delta)).coefficients

            err_locs.append(AlphaPoly(err_loc))

        return err_locs

    def find_errors(self, err_locs: list[AlphaPoly]) -> list[list[int]]:
        err_pos_list = []
        for err_loc in err_locs:
            err_pos = []
            for i in range(2 ** self.M - 1):
                if err_loc.replace_x_and_count(Alpha(i)) == Alpha(None):
                    err_pos.append((i - 1) % (2 ** self.M))

            err_pos_list.append(err_pos)

        return err_pos_list

    def find_error_evaluator(self, syndromes_list, err_locs):
        error_evaluators = []
        for (syndromes, err_loc) in zip(syndromes_list, err_locs):
            error_evaluator = (syndromes * err_loc)
            error_evaluators.append(error_evaluator)

        return error_evaluators

    def find_error_magnitude(self, err_locs: list[AlphaPoly], err_positions: list[list[int]],
                             error_evaluators: list[AlphaPoly]) -> list[AlphaPoly]:
        magnitudes_list = []
        for (err_loc, err_pos, error_evaluator) in zip(err_locs, err_positions, error_evaluators):
            # Pochodna formalna lokatora błędów

            test = []
            for i, coef in enumerate(err_loc.coefficients):
                if (len(err_loc.coefficients) - i - 1) % 2 == 1:
                    test.append(coef)
                else:
                    test.append(None)

            err_loc_derivative = AlphaPoly(test)

            err_loc_derivative = err_loc_derivative.get_cyclic_shifted(1, 'right').get_trimmed()

            print("Error locator derivative (Lambda'):", err_loc_derivative)

            magnitudes = []
            for pos in err_pos:
                # Odwrotność pozycji błędu
                alpha_neg_pos = Alpha(pos).get_inverse() if pos is not None else Alpha(None)

                # Oblicz wartości wielomianów w x_i^-1
                numerator = error_evaluator.replace_x_and_count(alpha_neg_pos)
                denominator = err_loc_derivative.replace_x_and_count(alpha_neg_pos)
                print("Numerator (Omega):", numerator)
                print("Denominator (Lambda'):", denominator)

                # Magnitude błędu
                magnitude = numerator / denominator
                magnitudes.append(magnitude)

            # Dodaj wielomian magnitudy
            magnitudes_list.append(AlphaPoly([x.power for x in magnitudes]))

        return magnitudes_list
