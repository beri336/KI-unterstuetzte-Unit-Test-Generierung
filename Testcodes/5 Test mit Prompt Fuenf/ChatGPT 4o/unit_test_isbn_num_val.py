import unittest
from isbn_num_val import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):

    # Normal Input Cases
    def test_valid_ISBN10(self):
        """Test a valid ISBN-10."""
        self.assertTrue(valid_ISBN10("0471958697"))  # Valid ISBN-10 example

    def test_valid_ISBN10_with_X(self):
        """Test a valid ISBN-10 with 'X' as the check digit."""
        self.assertTrue(valid_ISBN10("0306406152"))  # Valid ISBN-10 with 'X'

    def test_valid_ISBN13(self):
        """Test a valid ISBN-13."""
        self.assertTrue(valid_ISBN13("9780306406157"))  # Valid ISBN-13 example

    def test_valid_ISBN_function(self):
        """Test the valid_ISBN function with correct ISBN-10 and ISBN-13."""
        self.assertTrue(valid_ISBN("0471958697"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("9780306406157"))  # Valid ISBN-13

    def test_validate_isbn_function_valid(self):
        """Test validate_isbn function for valid cases."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780306406157"), "Valid ISBN number.")

    # Edge Cases
    def test_valid_ISBN10_invalid_format(self):
        """Test ISBN-10 with invalid format (non-numeric characters)."""
        self.assertFalse(valid_ISBN10("04719X8697"))  # Invalid format

    def test_valid_ISBN10_short_length(self):
        """Test ISBN-10 with fewer than 10 characters."""
        self.assertFalse(valid_ISBN10("04719586"))  # Too short

    def test_valid_ISBN13_short_length(self):
        """Test ISBN-13 with fewer than 13 characters."""
        self.assertFalse(valid_ISBN13("97803064061"))  # Too short

    def test_valid_ISBN13_invalid_format(self):
        """Test ISBN-13 with invalid characters."""
        self.assertFalse(valid_ISBN13("9780X06406157"))  # Invalid format

    def test_valid_ISBN_mixed_format(self):
        """Test valid_ISBN function with mixed formats."""
        self.assertFalse(valid_ISBN("9780306406X57"))  # Invalid check digit

    def test_validate_isbn_invalid_format(self):
        """Test validate_isbn function with invalid formats."""
        self.assertEqual(validate_isbn("9780306406X57"), "Invalid ISBN number.")
        self.assertEqual(validate_isbn("04719586"), "Invalid ISBN number.")

    # Invalid Input Cases
    def test_valid_ISBN_invalid_type(self):
        """Test valid_ISBN with non-string inputs."""
        with self.assertRaises(AttributeError):  # replace("-", "") on non-string
            valid_ISBN(1234567890)

    def test_valid_ISBN10_invalid_type(self):
        """Test valid_ISBN10 with non-string inputs."""
        with self.assertRaises(TypeError):  # Iteration on non-string
            valid_ISBN10(1234567890)

    def test_valid_ISBN13_invalid_type(self):
        """Test valid_ISBN13 with non-string inputs."""
        with self.assertRaises(TypeError):  # Iteration on non-string
            valid_ISBN13(9780306406157)

    def test_validate_isbn_invalid_type(self):
        """Test validate_isbn with non-string inputs."""
        with self.assertRaises(AttributeError):  # replace("-", "") on non-string
            validate_isbn(9780306406157)

    def test_valid_ISBN_empty_string(self):
        """Test valid_ISBN with an empty string."""
        self.assertFalse(valid_ISBN(""))

    def test_valid_ISBN10_empty_string(self):
        """Test valid_ISBN10 with an empty string."""
        self.assertFalse(valid_ISBN10(""))

    def test_valid_ISBN13_empty_string(self):
        """Test valid_ISBN13 with an empty string."""
        self.assertFalse(valid_ISBN13(""))

if __name__ == "__main__":
    unittest.main()