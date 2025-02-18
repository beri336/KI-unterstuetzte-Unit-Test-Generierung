import unittest
from isbn_num_val import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):
    # Tests for valid_ISBN
    def test_valid_ISBN_valid_ISBN10(self):
        self.assertTrue(valid_ISBN("0471958697"))

    def test_valid_ISBN_valid_ISBN13(self):
        self.assertTrue(valid_ISBN("9780470059029"))

    def test_valid_ISBN_invalid_length(self):
        self.assertFalse(valid_ISBN("123456789"))

    def test_valid_ISBN_invalid_characters(self):
        self.assertFalse(valid_ISBN("ISBN123456X"))

    # Tests for valid_ISBN10
    def test_valid_ISBN10_valid(self):
        self.assertTrue(valid_ISBN10("0471958697"))

    def test_valid_ISBN10_invalid_check_digit(self):
        self.assertFalse(valid_ISBN10("0471958696"))

    def test_valid_ISBN10_invalid_format(self):
        self.assertFalse(valid_ISBN10("04719A8697"))

    def test_valid_ISBN10_check_digit_X(self):
        self.assertTrue(valid_ISBN10("0306406152"))

    # Tests for valid_ISBN13
    def test_valid_ISBN13_valid(self):
        self.assertTrue(valid_ISBN13("9780470059029"))

    def test_valid_ISBN13_invalid_check_digit(self):
        self.assertFalse(valid_ISBN13("9780470059028"))

    def test_valid_ISBN13_invalid_format(self):
        self.assertFalse(valid_ISBN13("97804700A9029"))

    # Tests for validate_isbn
    def test_validate_isbn_valid_ISBN10(self):
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")

    def test_validate_isbn_valid_ISBN13(self):
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")

    def test_validate_isbn_invalid(self):
        self.assertEqual(validate_isbn("1234567890"), "Invalid ISBN number.")