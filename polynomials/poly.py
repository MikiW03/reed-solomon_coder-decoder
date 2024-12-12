from abc import ABC, abstractmethod


class Poly(ABC):
    coefficients: list[int | None] = None

    @abstractmethod
    def __str__(self):
        pass

    def __len__(self):
        return len(self.coefficients)

    @abstractmethod
    def __repr__(self):
        pass

    def __eq__(self, other):
        return str(self.get_trimmed()) == str(other.get_trimmed())

    def get_degree(self):
        return len(self.coefficients) - 1

    @abstractmethod
    def get_trimmed(self):
        pass

    @abstractmethod
    def get_filled(self, desired_no_of_bits: int):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __mod__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass
