import unittest
from main import convert_number  # Import the function to be tested

class TestNumberConversion(unittest.TestCase):
    def test_common_values(self):
        """
        Test normal input cases with common values.
        """
        self.assertEqual(convert_number(1000), "One Thousand")
        self.assertEqual(convert_number(1234), "One Thousand Two Hundred Thirty Four")
        self.assertEqual(convert_number(5678), "Five Hundred Sixty Seven Eight")

    def test_edge_cases(self):
        """
        Test edge cases (e.g., empty lists, negative numbers, etc.).
        """
        # Negative numbers
        with self.assertRaises(ValueError):
            convert_number(-1234)
        
        # Zero
        self.assertEqual(convert_number(0), "Zero")
        self.assertEqual(convert_number(10**12), 'This program supports a maximum of 12 digit numbers.')

    def test_invalid_input_cases(self):
        """
        Test invalid input cases that should raise exceptions.
        """
        with self.assertRaises(TypeError):
            convert_number("1234")  # Input is not an integer
        with self.assertRaises(TypeError):
            convert_number(123.45)  # Input is a float
        with self.assertRaises(ValueError):
            convert_number(-1000)  # Negative number

if __name__ == '__main__':
    unittest.main()
def convert_number(number):
    """
    Convert a number to its word representation.
    :param number: Integer to convert.
    :return: Word representation of the number.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")
    if number < 0:
        raise ValueError("Input must be non-negative.")

    return f"{number} in words is: {convert_to_words(number)}"
def convert_to_words(number):
    """
    Convert a number into its English word representation.
    :param number: Integer number to be converted.
    :return: Words representing the number.
    """
    length = len(str(number))
    if length > 12:
        return 'This program supports a maximum of 12 digit numbers.'

    count = length // 3 if length % 3 == 0 else length // 3 + 1
    copy = count
    words = []

    for i in range(length - 1, -1, -3):
        words.append(fetch_words(
            str(number)[0 if i - 2 < 0 else i - 2 : i + 1], copy - count))
        count -= 1

    final_words = ''
    for s in reversed(words):
        final_words += (s + ' ')

    return final_words.strip()