import unittest
from isbn_validation import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):

    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN10("0470956528"))

    def test_invalid_isbn10(self):
        self.assertFalse(valid_ISBN10("1234567890"))
        self.assertFalse(valid_ISBN10("0470956532"))  # '2' is not a valid check digit for ISBN-10

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN13("9780747533997"))

    def test_invalid_isbn13(self):
        self.assertFalse(valid_ISBN13("123456789012"))
        self.assertFalse(valid_ISBN13("9780747533996"))  # '6' is not a valid check digit for ISBN-13

    def test_valid_isbn_10_and_13(self):
        self.assertTrue(valid_ISBN("0470956528"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("9780747533997"))  # Valid ISBN-13

    def test_empty_string(self):
        self.assertFalse(valid_ISBN(""))

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            valid_ISBN(None)
        with self.assertRaises(TypeError):
            valid_ISBN([1, 2, 3])

    def test_validate_isbn(self):
        self.assertEqual(validate_isbn("0470956528"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780747533997"), "Valid ISBN number.")

        self.assertEqual(validate_isbn("1234567890"), "Invalid ISBN number.")
        self.assertEqual(validate_isbn("abcde"), "Invalid ISBN number.")

if __name__ == "__main__":
    unittest.main()