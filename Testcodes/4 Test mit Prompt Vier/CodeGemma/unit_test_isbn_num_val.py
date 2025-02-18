import unittest

class TestValidISBN(unittest.TestCase):

    def test_valid_isbn10_valid_input(self):
        self.assertTrue(valid_ISBN("0307245347"))

    def test_valid_isbn13_valid_input(self):
        self.assertTrue(valid_ISBN("9780307245346"))

    def test_invalid_isbn_wrong_length(self):
        self.assertFalse(valid_ISBN("030724534"))

    def test_invalid_isbn10_invalid_format(self):
        self.assertFalse(valid_ISBN("a307245347"))

    def test_invalid_isbn13_invalid_format(self):
        self.assertFalse(valid_ISBN("978a307245346"))

    def test_valid_isbn10_check_digit_x(self):
        self.assertTrue(valid_ISBN("030724534X"))

    def test_invalid_isbn13_check_digit(self):
        self.assertFalse(valid_ISBN("9780307245345"))

    def test_validate_isbn_valid_input(self):
        self.assertEqual(validate_isbn("0307245347"), "Valid ISBN number.")

    def test_validate_isbn_invalid_input(self):
        self.assertEqual(validate_isbn("invalid_isbn"), "Invalid ISBN number.")

if __name__ == '__main__':
    unittest.main()