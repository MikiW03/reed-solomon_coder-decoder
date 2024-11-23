from unittest import TestCase

from alpha import Alpha


class TestAlpha(TestCase):
    zero = Alpha()
    a0 = Alpha(0)
    a1 = Alpha(1)
    a2 = Alpha(2)
    a3 = Alpha(3)
    a62 = Alpha(62)

    def test_addition(self):
        self.assertEqual(self.a1 + self.a2, Alpha(7))
        self.assertEqual(self.a62 + self.a3, Alpha(23))
        self.assertEqual(self.a62 + self.zero, Alpha(62))

    def test_multiplication(self):
        self.assertEqual(self.a1 * self.a2, Alpha(3))
        self.assertEqual(self.a62 * self.a3, Alpha(2))
        self.assertEqual(self.a62 * self.zero, Alpha())

    def test_get_inverse(self):
        self.assertEqual(self.a3.get_inverse(), Alpha(60))
        self.assertEqual(self.a2.get_inverse(), Alpha(61))
        self.assertEqual(self.a62.get_inverse(), Alpha(1))
