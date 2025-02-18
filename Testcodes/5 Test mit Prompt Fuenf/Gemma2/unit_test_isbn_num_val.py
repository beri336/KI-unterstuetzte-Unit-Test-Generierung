import unittest

from main import validate_isbn  # Import the function to be tested

class TestValidateISBN(unittest.TestCase):

    def test_valid_isbn10(self):
        """Test valid 10-digit ISBN."""
        self.assertEqual(validate_isbn("0-486-29375-X"), "Valid ISBN number.")
    
    def test_valid_isbn13(self):
        """Test valid 13-digit ISBN."""
        self.assertEqual(validate_isbn("978-0-306-40615-7"), "Valid ISBN number.")

    def test_invalid_isbn10(self):
        """Test invalid 10-digit ISBN."""
        self.assertEqual(validate_isbn("0-486-29375-Y"), "Invalid ISBN number.")

    def test_invalid_isbn13(self):
        """Test invalid 13-digit ISBN."""
        self.assertEqual(validate_isbn("978-0-306-40615-8"), "Invalid ISBN number.")

    def test_empty_isbn(self):
        """Test empty ISBN."""
        self.assertEqual(validate_isbn(""), "Invalid ISBN number.")
        

    def test_non_numeric_isbn(self):
        """Test ISBN with non-numeric characters."""
        self.assertEqual(validate_isbn("abc"), "Invalid ISBN number.")


if __name__ == '__main__':
    unittest.main()
   self.assertEqual(validate_isbn("0-486-29375-X"), "Valid ISBN number.") 