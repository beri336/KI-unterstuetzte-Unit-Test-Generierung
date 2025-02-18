import unittest

class TestISBNValidator(unittest.TestCase):

    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN('9780132350884'))
        self.assertTrue(valid_ISBN('047148642X'))

    def test_invalid_isbn10(self):
        self.assertFalse(valid_ISBN('9780132350883'))
        self.assertFalse(valid_ISBN('0471486420'))

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN('9780300174543'))
        self.assertTrue(valid_ISBN('9780132350884'))

    def test_invalid_isbn13(self):
        self.assertFalse(valid_ISBN('9780300174544'))
        self.assertFalse(valid_ISBN('9780132350883'))

    def test_invalid_isbn(self):
        self.assertFalse(valid_ISBN('invalid'))
        self.assertFalse(valid_ISBN(''))

    def test_validate_isbn(self):
        self.assertEqual(validate_isbn('9780132350884'), 'Valid ISBN number.')
        self.assertEqual(validate_isbn('invalid'), 'Invalid ISBN number.')

if __name__ == '__main__':
    unittest.main()