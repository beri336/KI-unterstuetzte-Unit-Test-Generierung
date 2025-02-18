import unittest

from your_module import *  # Replace 'your_module' with the actual module name

class TestISBNValidation(unittest.TestCase):

    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN("0-451-49827-1")) 
        self.assertFalse(valid_ISBN("0-451-49827-X1"))  # Invalid check digit

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN("978-0-451-49827-1")) 
        self.assertFalse(valid_ISBN("978-0-451-49827-2"))  # Invalid check digit

    def test_invalid_isbn_length(self):
        self.assertFalse(valid_ISBN("123456789")) # Not 10 or 13 digits
        self.assertFalse(valid_ISBN("123456789012345"))  # Too long

    def test_invalid_isbn_format(self):
        self.assertFalse(valid_ISBN("abc-1234567890")) # Letters in ISBN
        self.assertFalse(valid_ISBN("123 456 7890"))  # Spaces in ISBN

    def test_validate_isbn(self):
        self.assertEqual(validate_isbn("0-451-49827-1"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("978-0-451-49827-1"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("abc-1234567890"), "Invalid ISBN number.")


if __name__ == '__main__':
    unittest.main() 
