from unittest import TestCase

from alpha import Alpha
from polynomials.alpha_poly import AlphaPoly


class TestAlphaPoly(TestCase):
    p1 = AlphaPoly([5, 62, 1, None, None, 1])
    p2 = AlphaPoly([None, None, 2, 6, 1, 32, 51, 12])
    p3 = AlphaPoly([1, 3, 62])
    p4 = AlphaPoly([2, None])
    p5 = AlphaPoly([12, 1, 13, 9, None, 51, 60, 12, 5, 1, 0, 39, 5, 62, 1, None, None, 1])
    p6 = AlphaPoly([None, None, 62, 12, 31, 9, 12, 5, None, 13])

    def test_get_trimmed(self):
        self.assertEqual(len(self.p2.get_trimmed().coefficients), 6)
        self.assertEqual(len(self.p1.get_trimmed().alphas), 6)

    def test_get_filled(self):
        p1_filled = self.p1.get_filled(20)
        self.assertEqual(len(p1_filled.coefficients), 20)
        self.assertEqual(len(p1_filled.alphas), 20)
        self.assertEqual(p1_filled.coefficients[0], None)
        self.assertEqual(p1_filled.alphas[0], Alpha())

    def test_addition(self):
        self.assertEqual(self.p3 + self.p4, AlphaPoly([1, 8, 62]))

    def test_multiplication(self):
        self.assertEqual(self.p3 * self.p4, AlphaPoly([3, 5, 1, None]))

    def test_division(self):
        self.assertEqual(self.p1 / self.p2, AlphaPoly([3]))
        self.assertEqual(self.p2 / self.p3, AlphaPoly([1, 15, 7, 43]))
        self.assertEqual(self.p3 / self.p4, AlphaPoly([62, 1]))
        self.assertEqual(self.p1 / self.p4, AlphaPoly([3, 60, 62, None, None]))
        self.assertEqual(self.p1 / self.p3, AlphaPoly([4, 46, 3, 48]))
        self.assertEqual(self.p5 / self.p6, AlphaPoly([13, 6, 16, 42, 43, 55, 20, 39, 23, 34, 44]))
        self.assertEqual(AlphaPoly([40, None, 1]) / AlphaPoly([32, 61, 15]), AlphaPoly([8]))

    def test_modulo(self):
        self.assertEqual(self.p1 % self.p2, AlphaPoly([60, 33, 35, 54, 53]))
        self.assertEqual(self.p2 % self.p3, AlphaPoly([49, 58]))
        self.assertEqual(self.p3 % self.p4, AlphaPoly([62]))
        self.assertEqual(self.p1 % self.p4, AlphaPoly([1]))
        self.assertEqual(self.p1 % self.p3, AlphaPoly([40, 31]))
        self.assertEqual(self.p5 % self.p6, AlphaPoly([46, 14, 43, 57, 8, 47, 20]))
        self.assertEqual(AlphaPoly([40, None, 1]) % AlphaPoly([32, 61, 15]), AlphaPoly([6, 51]))
