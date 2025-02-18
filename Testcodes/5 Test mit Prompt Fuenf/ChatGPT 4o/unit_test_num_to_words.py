import unittest
from number_to_words import convert_to_words, convert_number, fetch_words


class TestNumberToWords(unittest.TestCase):

    # Normal Input Cases
    def test_single_digit(self):
        """Test single-digit numbers."""
        self.assertEqual(convert_to_words(5), "Five")
        self.assertEqual(convert_to_words(0), "Zero")

    def test_two_digits(self):
        """Test two-digit numbers."""
        self.assertEqual(convert_to_words(15), "Fifteen")
        self.assertEqual(convert_to_words(45), "Forty Five")

    def test_three_digits(self):
        """Test three-digit numbers."""
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(900), "Nine Hundred")

    def test_large_numbers(self):
        """Test large numbers with thousands, millions, and billions."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(123456789), 
                         "One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine")

    def test_convert_number_function(self):
        """Test the convert_number function."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    # Edge Cases
    def test_zero(self):
        """Test the number zero."""
        self.assertEqual(convert_to_words(0), "Zero")

    def test_hundred_boundary(self):
        """Test numbers at the boundary of hundreds."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_thousand_boundary(self):
        """Test numbers at the boundary of thousands."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(1999), "One Thousand Nine Hundred Ninety Nine")

    def test_maximum_supported_number(self):
        """Test the maximum supported number (12 digits)."""
        self.assertEqual(convert_to_words(999999999999), 
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_exceeding_max_digits(self):
        """Test numbers exceeding the maximum supported digits."""
        self.assertEqual(convert_to_words(1000000000000), 
                         "This program supports a maximum of 12 digit numbers.")

    def test_fetch_words_function(self):
        """Test the fetch_words function with three-digit blocks."""
        self.assertEqual(fetch_words("123", 0), "One Hundred Twenty Three ")
        self.assertEqual(fetch_words("007", 0), "Seven ")
        self.assertEqual(fetch_words("500", 1), "Five Hundred Thousand")

    # Invalid Input Cases
    def test_negative_number(self):
        """Test with a negative number."""
        with self.assertRaises(ValueError):
            convert_to_words(-123)

    def test_non_integer_input(self):
        """Test with non-integer inputs."""
        with self.assertRaises(ValueError):
            convert_to_words("123")

    def test_empty_input(self):
        """Test with empty input."""
        with self.assertRaises(TypeError):  # Expected since the function expects an integer
            convert_to_words()

    def test_large_number_boundary(self):
        """Test exactly 12-digit number to ensure it works."""
        self.assertEqual(convert_to_words(999999999999), 
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

if __name__ == "__main__":
    unittest.main()