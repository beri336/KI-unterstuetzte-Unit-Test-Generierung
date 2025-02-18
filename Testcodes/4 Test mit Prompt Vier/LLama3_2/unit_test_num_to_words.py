import unittest
from main import ones, twos, tens, suffixes, fetch_words, convert_to_words, convert_number

class TestNumberConversionFunctions(unittest.TestCase):

    def test_fetch_words_valid_input(self):
        # Test fetching words for a valid input number
        result = fetch_words('120', 0)
        self.assertEqual(result, 'One Hundred Two')

    def test_fetch_words_invalid_input(self):
        # Test fetching words for an invalid input (single digit)
        with self.assertRaises(IndexError):
            fetch_words('1', 0)

    def test_fetch_words_hundred_suffix(self):
        # Test fetching words with the hundred suffix
        result = fetch_words('100', 1)
        self.assertEqual(result, 'Hundred Thousand')

    def test_fetch_words_zero_suffix(self):
        # Test fetching words with the zero suffix
        result = fetch_words('10', 2)
        self.assertEqual(result, 'Ten Thousand')

class TestConvertToWordsFunctions(unittest.TestCase):

    def test_convert_to_words_valid_input(self):
        # Test converting a number to words for a valid input
        result = convert_to_words(123456789012)
        self.assertEqual(result, 'One Hundred Twenty Three Billion Forty Five Hundred Sixty Seven Million Eight Hundred Nine Thousand Twelve')

    def test_convert_to_words_invalid_input(self):
        # Test converting a number to words for an invalid input (more than 12 digits)
        result = convert_to_words(12345678901234567890)
        self.assertEqual(result, 'This program supports a maximum of 12 digit numbers.')

class TestConvertNumberFunctions(unittest.TestCase):

    def test_convert_number_valid_input(self):
        # Test converting a number to words and the word representation
        input_number = 1234567890
        result = convert_number(input_number)
        self.assertEqual(result, f"{input_number} in words is: One Billion Two Hundred Thirty Four Million Five Hundred Sixty Eight Thousand Nine Hundred")

    def test_convert_number_invalid_input(self):
        # Test converting an invalid number (non-integer)
        with self.assertRaises(TypeError):
            convert_number('1234567890')

if __name__ == '__main__':
    unittest.main()