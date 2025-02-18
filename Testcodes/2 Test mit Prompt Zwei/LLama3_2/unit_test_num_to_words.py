import unittest
from your_module import convert_number, fetch_words, ones, twos, tens, suffixes  # Replace 'your_module' with the actual name of the module containing the functions.

class TestNumberToWords(unittest.TestCase):

    def test_simple_numbers(self):
        # Testing simple numbers
        self.assertEqual(convert_number(100), "One Hundred")
        self.assertEqual(convert_number(12345), "Twelve Thousand, Three Hundred and Forty-Five")
        self.assertEqual(convert_number(67890), "Sixty-Eighty-Nine Thousand")

    def test_complex_numbers(self):
        # Testing complex numbers
        self.assertEqual(convert_number(1110000), 'One Million One Hundred Eleven Thousand')
        self.assertEqual(convert_number(1234567890123), 'Twelve Billion, Three Hundred and Forty-Five Million Six Hundred and Seventy-Eight Thousand, Twelve')

    def test_zeros(self):
        # Testing zero as a number
        self.assertEqual(convert_number(0), "Zero")
        self.assertEqual(convert_number(-0), "Zero")  # Negative zeros should also be converted to words

    def test_hundred_suffix(self):
        # Testing hundred suffix correctly
        self.assertEqual(fetch_words('100', 0), 'One Hundred')
        self.assertEqual(fetch_words('101', 1), 'One Hundred and One')

    def test_tens_suffix(self):
        # Testing tens suffix correctly
        self.assertEqual(fetch_words('120', 1), 'One Hundred and Twenty')
        self.assertEqual(fetch_words('130', 1), 'One Hundred and Thirty')

    def test_thousands_suffix(self):
        # Testing thousand suffix correctly
        self.assertEqual(fetch_words('1234', 2), "Twelve Thousand, Three Hundred and Forty-Four")
        self.assertEqual(fetch_words('1500', 3), "One Million Five Hundred")

    def test_larger_numbers(self):
        # Testing larger numbers correctly
        self.assertEqual(convert_number(10000000), 'Ten Million')
        self.assertEqual(convert_number(123456789012), 'Twelve Billion, Three Hundred and Forty-Five Million Six Hundred and Seventy-Eight Thousand, Twelve')

    def test_invalid_numbers(self):
        # Testing invalid numbers
        with self.assertRaises(ValueError):  # Assuming the function that converts to words will raise a ValueError for invalid inputs
            convert_number(-1000)
            convert_number(12345678901234)  # This should be out of range due to integer limit

    def test_max_numbers(self):
        # Testing maximum numbers
        self.assertEqual(convert_number(999999), 'Nine Hundred and Ninety-Nine Thousand, Nine')
        self.assertEqual(convert_number(10000000), 'Ten Million')

if __name__ == '__main__':
    unittest.main()