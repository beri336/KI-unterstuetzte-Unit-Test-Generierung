import unittest
from your_module import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):

    def test_valid_ISBN10(self):
        """Test cases for valid ISBN-10."""
        self.assertTrue(valid_ISBN10("0471958697"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN10("0-321-14653-0".replace('-', '')), "Should return True for valid ISBN-10 with hyphens.")
        self.assertTrue(valid_ISBN10("0306406152"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN10("359821508X"), "Should return True for valid ISBN-10 ending with X.")
        self.assertFalse(valid_ISBN10("0471958698"), "Should return False for invalid ISBN-10.")
        self.assertFalse(valid_ISBN10("1234567890"), "Should return False for invalid ISBN-10.")
        self.assertFalse(valid_ISBN10("047195869X"), "Should return False for invalid check digit.")

    def test_valid_ISBN13(self):
        """Test cases for valid ISBN-13."""
        self.assertTrue(valid_ISBN13("9780470059029"), "Should return True for valid ISBN-13.")
        self.assertTrue(valid_ISBN13("978-0-13-149505-0".replace('-', '')), "Should return True for valid ISBN-13 with hyphens.")
        self.assertTrue(valid_ISBN13("9780306406157"), "Should return True for valid ISBN-13.")
        self.assertFalse(valid_ISBN13("9780470059028"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN13("9780306406156"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN13("97804700590"), "Should return False for incomplete ISBN-13.")

    def test_valid_ISBN(self):
        """Test cases for the combined ISBN validation function."""
        self.assertTrue(valid_ISBN("0471958697"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN("9780470059029"), "Should return True for valid ISBN-13.")
        self.assertFalse(valid_ISBN("123456789"), "Should return False for invalid length.")
        self.assertFalse(valid_ISBN("9780470059028"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN("0471958698"), "Should return False for invalid ISBN-10.")

    def test_validate_isbn(self):
        """Test cases for validate_isbn function."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.", "Should return 'Valid ISBN number.' for valid ISBN-10.")
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.", "Should return 'Valid ISBN number.' for valid ISBN-13.")
        self.assertEqual(validate_isbn("123456789"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid length.")
        self.assertEqual(validate_isbn("9780470059028"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid ISBN-13.")
        self.assertEqual(validate_isbn("0471958698"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid ISBN-10.")

if __name__ == '__main__':
    unittest.main()