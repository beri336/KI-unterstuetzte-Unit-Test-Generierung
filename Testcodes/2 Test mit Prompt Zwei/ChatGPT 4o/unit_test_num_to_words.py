import unittest
from your_script_name import convert_to_words, fetch_words

class TestNumberToWords(unittest.TestCase):
    def test_single_digit(self):
        """Test single-digit numbers."""
        for i in range(10):
            self.assertEqual(convert_to_words(i), f"{ones[i]}")

    def test_two_digits(self):
        """Test two-digit numbers."""
        self.assertEqual(convert_to_words(10), "Ten")
        self.assertEqual(convert_to_words(11), "Eleven")
        self.assertEqual(convert_to_words(19), "Nineteen")
        self.assertEqual(convert_to_words(21), "Twenty One")
        self.assertEqual(convert_to_words(99), "Ninety Nine")

    def test_three_digits(self):
        """Test three-digit numbers."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(105), "One Hundred Five")
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_thousands(self):
        """Test numbers in the thousands."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(12345), "Twelve Thousand Three Hundred Forty Five")
        self.assertEqual(convert_to_words(10000), "Ten Thousand")
        self.assertEqual(convert_to_words(10101), "Ten Thousand One Hundred One")

    def test_millions(self):
        """Test numbers in the millions."""
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(1234567), "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven")
        self.assertEqual(convert_to_words(1001000), "One Million One Thousand")

    def test_billions(self):
        """Test numbers in the billions."""
        self.assertEqual(convert_to_words(1000000000), "One Billion")
        self.assertEqual(convert_to_words(987654321), "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_large_numbers(self):
        """Test numbers beyond the supported range."""
        self.assertEqual(convert_to_words(123456789012), "One Hundred Twenty Three Billion Four Hundred Fifty Six Million Seven Hundred Eighty Nine Thousand Twelve")
        self.assertEqual(convert_to_words(1000000000000), "This program supports a maximum of 12 digit numbers.")

    def test_fetch_words_edge_cases(self):
        """Test edge cases for fetch_words."""
        self.assertEqual(fetch_words("000", 0), "Zero")
        self.assertEqual(fetch_words("001", 0), "One")
        self.assertEqual(fetch_words("010", 0), "Ten")
        self.assertEqual(fetch_words("100", 0), "One Hundred ")
        self.assertEqual(fetch_words("101", 0), "One Hundred One ")

    def test_zero_handling(self):
        """Test the handling of zero."""
        self.assertEqual(convert_to_words(0), "Zero")

    def test_leading_zeros(self):
        """Test numbers with leading zeros."""
        self.assertEqual(convert_to_words(int("0000123")), "One Hundred Twenty Three")
        self.assertEqual(fetch_words("012", 0), "Twelve")

    def test_invalid_inputs(self):
        """Test invalid inputs."""
        with self.assertRaises(ValueError):
            convert_to_words("abc")  # Non-integer
        with self.assertRaises(ValueError):
            convert_to_words(-123)  # Negative number

if __name__ == "__main__":
    unittest.main()