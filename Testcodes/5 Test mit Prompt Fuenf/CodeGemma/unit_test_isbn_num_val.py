import unittest

class TestValidISBN(unittest.TestCase):

    # Test normal input cases with common values
    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN('9780132350884'))
        self.assertTrue(valid_ISBN('0470059348'))

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN('9780132350884'))
        self.assertTrue(valid_ISBN('9780470059344'))

    # Test edge cases
    def test_invalid_isbn10(self):
        self.assertFalse(valid_ISBN('013235088X'))
        self.assertFalse(valid_ISBN('0470059347'))

    def test_invalid_isbn13(self):
        self.assertFalse(valid_ISBN('9780132350883'))
        self.assertFalse(valid_ISBN('9780470059343'))

    # Test invalid input cases that should raise exceptions
    def test_invalid_isbn_format(self):
        with self.assertRaises(ValueError):
            valid_ISBN('a1b2c3d4e5f6g7h8')

    def test_invalid_isbn_length(self):
        with self.assertRaises(ValueError):
            valid_ISBN('123456789012345')

if __name__ == '__main__':
    unittest.main()