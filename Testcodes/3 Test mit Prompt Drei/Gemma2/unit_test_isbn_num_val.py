import unittest

class TestValidateISBN(unittest.TestCase):

    def test_valid_isbn10(self):
        # Positive case - Valid 10-digit ISBN
        self.assertEqual(validate_isbn("0-306-40615-7"), "Valid ISBN number.")

    def test_valid_isbn13(self):
        # Positive case - Valid 13-digit ISBN
        self.assertEqual(validate_isbn("978-0-306-40615-7"), "Valid ISBN number.")

    def test_invalid_length(self):
        # Edge case - Invalid length (too short)
        self.assertEqual(validate_isbn("123456789"), "Invalid ISBN number.")

    def test_invalid_length_too_long(self):
        # Edge case - Invalid length (too long)
        self.assertEqual(validate_isbn("1234567890123456789"), "Invalid ISBN number.")

    def test_invalid_characters_isbn10(self):
        # Negative case - Invalid characters in ISBN-10
        self.assertEqual(validate_isbn("0-306-40615-8A"), "Invalid ISBN number.")

    def test_invalid_characters_isbn13(self):
        # Negative case - Invalid characters in ISBN-13
        self.assertEqual(validate_isbn("978-0-306-40615-7A"), "Invalid ISBN number.")

    def test_missing_hyphens_isbn10(self):
        # Edge case - Missing hyphens in ISBN-10
        self.assertEqual(validate_isbn("0306406157"), "Valid ISBN number.") 

    def test_missing_hyphens_isbn13(self):
        # Edge case - Missing hyphens in ISBN-13
        self.assertEqual(validate_isbn("9780306406157"), "Valid ISBN number.")   



if __name__ == '__main__':
    unittest.main()