import unittest
from your_module import convert_number, convert_to_words

class TestNumberToWords(unittest.TestCase):
    # Positive Test Cases
    def test_single_digits(self):
        """Test conversion of single-digit numbers."""
        self.assertEqual(convert_to_words(0), "Zero")
        self.assertEqual(convert_to_words(5), "Five")

    def test_two_digits(self):
        """Test conversion of two-digit numbers."""
        self.assertEqual(convert_to_words(10), "Ten")
        self.assertEqual(convert_to_words(25), "Twenty Five")
        self.assertEqual(convert_to_words(99), "Ninety Nine")

    def test_three_digits(self):
        """Test conversion of three-digit numbers."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_large_numbers(self):
        """Test conversion of larger numbers."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(12345), "Twelve Thousand Three Hundred Forty Five")
        self.assertEqual(convert_to_words(987654321), 
                         "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_convert_number_output(self):
        """Test the `convert_number` function output."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    # Edge Cases
    def test_zero_padding(self):
        """Test numbers with leading zeros."""
        self.assertEqual(convert_to_words(7), "Seven")  # Leading zeros should not affect the output.

    def test_exact_suffix_boundaries(self):
        """Test numbers at boundaries of suffixes."""
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(1000000000), "One Billion")

    def test_minimum_and_maximum_supported_values(self):
        """Test the smallest and largest supported numbers."""
        self.assertEqual(convert_to_words(0), "Zero")
        self.assertEqual(
            convert_to_words(999999999999),
            "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine"
        )

    # Negative Test Cases
    def test_invalid_large_number(self):
        """Test numbers larger than 12 digits."""
        self.assertEqual(
            convert_to_words(1000000000000),
            "This program supports a maximum of 12 digit numbers."
        )

    def test_invalid_input_type(self):
        """Test invalid input types."""
        with self.assertRaises(ValueError):
            convert_to_words("abc")  # Strings should raise errors.
        with self.assertRaises(ValueError):
            convert_to_words(None)  # None should raise errors.

    def test_negative_numbers(self):
        """Test negative numbers."""
        with self.assertRaises(ValueError):
            convert_to_words(-123)  # Negative numbers should raise errors.

    # Performance Test Cases
    def test_large_number_performance(self):
        """Test performance with the largest supported number."""
        result = convert_to_words(999999999999)
        self.assertTrue(result.startswith("Nine Hundred Ninety Nine"))  # Ensures completion.

if __name__ == "__main__":
    unittest.main()