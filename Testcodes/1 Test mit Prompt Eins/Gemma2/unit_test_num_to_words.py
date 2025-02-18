import unittest

from your_module import convert_number  # Replace your_module with the actual module name


class TestNumberConversion(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")

    def test_single_digit(self):
        for i in range(1, 10):
            self.assertEqual(convert_number(i), f"{i} in words is: {ones[i]}")

    def test_tens_numbers(self):
        self.assertEqual(convert_number(10), "10 in words is: Ten")
        self.assertEqual(convert_number(25), "25 in words is: Twenty Five")
        self.assertEqual(convert_number(99), "99 in words is: Ninety Nine")

    def test_hundreds_numbers(self):
        self.assertEqual(convert_number(100), "100 in words is: One Hundred")
        self.assertEqual(convert_number(234), "234 in words is: Two Hundred Thirty Four")
        self.assertEqual(convert_number(999), "999 in words is: Nine Hundred Ninety Nine")

    def test_thousands_numbers(self):
        self.assertEqual(convert_number(1000), "1000 in words is: One Thousand")
        self.assertEqual(convert_number(2345), "2345 in words is: Two Thousand Three Hundred Forty Five")

    def test_larger_numbers(self):
        self.assertEqual(convert_number(1234567), "1234567 in words is: One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven")


if __name__ == '__main__':
    unittest.main()