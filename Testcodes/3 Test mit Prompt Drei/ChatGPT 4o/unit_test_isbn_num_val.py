import unittest
from your_module import valid_ISBN, validate_isbn

class TestISBNValidation(unittest.TestCase):

    # Positive Test Cases
    def test_valid_ISBN10(self):
        """Test valid ISBN-10."""
        self.assertTrue(valid_ISBN("0471958697"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("0-471-60695-2"))  # Valid with hyphens
        self.assertTrue(valid_ISBN("0 471 60695 2"))  # Valid with spaces
        self.assertTrue(valid_ISBN("0306406152"))  # Valid ISBN-10

    def test_valid_ISBN13(self):
        """Test valid ISBN-13."""
        self.assertTrue(valid_ISBN("9780470059029"))  # Valid ISBN-13
        self.assertTrue(valid_ISBN("978-0-13-149505-0"))  # Valid with hyphens
        self.assertTrue(valid_ISBN("978 0 471 48648 0"))  # Valid with spaces
        self.assertTrue(valid_ISBN("9783161484100"))  # Valid ISBN-13

    def test_validate_isbn_valid(self):
        """Test validation function for valid ISBNs."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")

    # Edge Cases
    def test_invalid_length(self):
        """Test invalid ISBNs with incorrect lengths."""
        self.assertFalse(valid_ISBN("123456789"))  # Too short
        self.assertFalse(valid_ISBN("12345678901234"))  # Too long

    def test_invalid_characters(self):
        """Test ISBNs with invalid characters."""
        self.assertFalse(valid_ISBN("04719A8697"))  # Invalid character in ISBN-10
        self.assertFalse(valid_ISBN("97804X0059029"))  # Invalid character in ISBN-13

    def test_ISBN10_invalid_check_digit(self):
        """Test ISBN-10 with invalid check digit."""
        self.assertFalse(valid_ISBN("0471958698"))  # Invalid check digit
        self.assertFalse(valid_ISBN("0306406153"))  # Invalid check digit

    def test_ISBN13_invalid_check_digit(self):
        """Test ISBN-13 with invalid check digit."""
        self.assertFalse(valid_ISBN("9780470059028"))  # Invalid check digit
        self.assertFalse(valid_ISBN("9783161484101"))  # Invalid check digit

    # Negative Test Cases
    def test_empty_input(self):
        """Test empty input."""
        self.assertFalse(valid_ISBN(""))
        self.assertEqual(validate_isbn(""), "Invalid ISBN number.")

    def test_only_hyphens_and_spaces(self):
        """Test ISBNs with only hyphens and spaces."""
        self.assertFalse(valid_ISBN("----"))
        self.assertFalse(valid_ISBN("    "))

    def test_invalid_types(self):
        """Test invalid data types as input."""
        with self.assertRaises(AttributeError):  # Strings expected
            valid_ISBN(None)
        with self.assertRaises(AttributeError):  # Strings expected
            valid_ISBN(9780470059029)  # Integer input

    # Performance Test Case
    def test_performance_with_large_input(self):
        """Test performance and handling of unusually large inputs."""
        large_input = "1" * 1000  # 1000 characters
        self.assertFalse(valid_ISBN(large_input))  # Should not validate as ISBN

if __name__ == "__main__":
    unittest.main()