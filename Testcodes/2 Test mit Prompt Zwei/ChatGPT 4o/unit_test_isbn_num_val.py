import unittest
from your_script_name import valid_ISBN, validate_isbn

class TestISBNValidation(unittest.TestCase):
    def test_valid_ISBN10(self):
        """Test valid ISBN-10 numbers."""
        self.assertTrue(valid_ISBN("0471958697"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("0-471-95869-7"))  # Valid ISBN-10 with hyphens
        self.assertTrue(valid_ISBN("047195869X"))  # Valid ISBN-10 with 'X' as check digit
    
    def test_invalid_ISBN10(self):
        """Test invalid ISBN-10 numbers."""
        self.assertFalse(valid_ISBN("0471958698"))  # Invalid checksum
        self.assertFalse(valid_ISBN("047195869"))  # Too short
        self.assertFalse(valid_ISBN("04719586999"))  # Too long
        self.assertFalse(valid_ISBN("04719586X7"))  # Invalid character placement
    
    def test_valid_ISBN13(self):
        """Test valid ISBN-13 numbers."""
        self.assertTrue(valid_ISBN("9780470059029"))  # Valid ISBN-13
        self.assertTrue(valid_ISBN("978-0-13-149505-0"))  # Valid ISBN-13 with hyphens
        self.assertTrue(valid_ISBN("978 0 471 48648 0"))  # Valid ISBN-13 with spaces
    
    def test_invalid_ISBN13(self):
        """Test invalid ISBN-13 numbers."""
        self.assertFalse(valid_ISBN("9780470059028"))  # Invalid checksum
        self.assertFalse(valid_ISBN("978047005902"))  # Too short
        self.assertFalse(valid_ISBN("97804700590299"))  # Too long
        self.assertFalse(valid_ISBN("97804700X9029"))  # Invalid character
    
    def test_edge_cases(self):
        """Test edge cases for ISBN validation."""
        self.assertFalse(valid_ISBN(""))  # Empty string
        self.assertFalse(valid_ISBN(" "))  # String with only spaces
        self.assertFalse(valid_ISBN("-"))  # Single hyphen
        self.assertFalse(valid_ISBN("1234567890"))  # Valid length but invalid ISBN-10 checksum
        self.assertFalse(valid_ISBN("1234567890123"))  # Valid length but invalid ISBN-13 checksum
    
    def test_validate_isbn_function(self):
        """Test the `validate_isbn` function."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("0471958698"), "Invalid ISBN number.")
        self.assertEqual(validate_isbn("9780470059028"), "Invalid ISBN number.")
    
    def test_invalid_characters(self):
        """Test ISBNs with invalid characters."""
        self.assertFalse(valid_ISBN("04719586#7"))  # Invalid character in ISBN-10
        self.assertFalse(valid_ISBN("97804@0059029"))  # Invalid character in ISBN-13
    
    def test_ISBN_with_mixed_delimiters(self):
        """Test ISBNs with mixed delimiters."""
        self.assertTrue(valid_ISBN("978-0 471-48648 0"))  # Mixed hyphens and spaces
        self.assertFalse(valid_ISBN("978-0 471-48648X"))  # Mixed delimiters with invalid check digit
    
    def test_ISBN_with_leading_trailing_spaces(self):
        """Test ISBNs with leading or trailing spaces."""
        self.assertTrue(valid_ISBN(" 9780470059029 "))  # Valid ISBN-13 with spaces
        self.assertTrue(valid_ISBN(" 0471958697 "))  # Valid ISBN-10 with spaces

if __name__ == "__main__":
    unittest.main()