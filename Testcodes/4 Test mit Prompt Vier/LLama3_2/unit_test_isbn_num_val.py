# zusammengefuegter Code #

import unittest

class TestISBNValidation(unittest.TestCase):
    pass  # placeholder for future tests
def test_valid_isbn(self):
    # Valid ISBN-10 number
    self.assertTrue(valid_ISBN("0345453747"))

    # Invalid ISBN-10 number (missing check digit)
    self.assertFalse(valid_ISBN("0345453746"))

    # Invalid ISBN-10 number (invalid format)
    self.assertFalse(valid_ISBN("1234567890X"))
def test_valid_isbn10(self):
    # Valid ISBN-10 number
    self.assertTrue(valid_ISBN10("0345453747"))

    # Invalid ISBN-10 number (missing check digit)
    self.assertFalse(valid_ISBN10("1234567890"))

    # Valid ISBN-10 number with 'X' as the last character
    self.assertTrue(valid_ISBN10("0345453747X"))

    # Invalid ISBN-10 number (invalid format)
    self.assertFalse(valid_ISBN10("1234567891X"))
def test_valid_isbn13(self):
    # Valid ISBN-13 number
    self.assertTrue(valid_ISBN13("9780345453747"))

    # Invalid ISBN-13 number (missing check digit)
    self.assertFalse(valid_ISBN13("1234567890123"))

    # Invalid ISBN-13 number (invalid format)
    self.assertFalse(valid_ISBN13("1234567890xyz"))
def test_validate_isbn(self):
    # Valid ISBN number
    self.assertEqual(validate_isbn("0345453747"), "Valid ISBN number.")

    # Invalid ISBN number (missing check digit)
    self.assertEqual(validate_isbn("1234567890"), "Invalid ISBN number.")

    # Empty string
    with self.assertRaises(ValueError):
        validate_isbn("")