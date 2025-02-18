import unittest

class TestISBNValidator(unittest.TestCase):

    # Special case test for an empty string
    def test_empty_string(self):
        self.assertFalse(valid_ISBN(''))

    # Edge case test for a hyphenated ISBN-10
    def test_hyphenated_isbn10(self):
        self.assertTrue(valid_ISBN10('0-3-6-5-2-8-9-7-1-4'))

    # Edge case test for an X in the middle of an ISBN-10
    def test_x_in_middle_isbn10(self):
        self.assertFalse(valid_ISBN10('0-3-X-6-5-2-8-9-7-1-4'))

    # Special case test for a hyphenated ISBN-13
    def test_hyphenated_isbn13(self):
        self.assertTrue(valid_ISBN13('3-6-27-15-63-42-17-22-93-56-81-20'))

    # Edge case test for an X in the middle of an ISBN-13
    def test_x_in_middle_isbn13(self):
        self.assertFalse(valid_ISBN13('3-6-X-27-15-63-42-17-22-93-56-81-20'))

    # Special case test for a hyphenated mixed ISBN (10 and 13)
    def test_hyphenated_mixed_isbn(self):
        self.assertFalse(valid_ISBN('0-3-6-5-2-8-9-7-1-4-3-6-27-15'))

    # Special case test for a valid ISBN-10 with hyphens
    def test_valid_isbn10_with_hyphens(self):
        self.assertTrue(valid_ISBN10('0-3-6-5-2-8-9-7-1-4'))

    # Special case test for a valid ISBN-13 with hyphens
    def test_valid_isbn13_with_hyphens(self):
        self.assertTrue(valid_ISBN13('3-6-27-15-63-42-17-22-93-56-81-20'))

    # Edge case test for an invalid ISBN-10 (non-digit characters)
    def test_invalid_isbn10_non_digit_characters(self):
        self.assertFalse(valid_ISBN10('0-3-6-5X-2-8-9-7-1-4'))

    # Edge case test for an invalid ISBN-13 (non-digit characters)
    def test_invalid_isbn13_non_digit_characters(self):
        self.assertFalse(valid_ISBN13('3-6-27-15-63-42-17-22-93-56-81-Z-20'))

    # Special case test for a valid ISBN
    def test_valid_isbn(self):
        self.assertTrue(valid_ISBN10('0-3-6-5-2-8-9-7-1-4'))
        self.assertTrue(valid_ISBN13('3-6-27-15-63-42-17-22-93-56-81-20'))

    # Special case test for an invalid ISBN
    def test_invalid_isbn(self):
        self.assertFalse(valid_ISBN10('0-3-6-5-2-8-9-7-1-4-'))
        self.assertFalse(valid_ISBN13('3-6-27-15-63-42-17-22-93-56-81-20-'))

    def test_validate_isbn(self):
        self.assertEqual(validate_isbn("0-3-6-5-2-8-9-7-1-4"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("0-3-6-5-2-8-9-7-1-4-"), "Invalid ISBN number.")

if __name__ == '__main__':
    unittest.main()