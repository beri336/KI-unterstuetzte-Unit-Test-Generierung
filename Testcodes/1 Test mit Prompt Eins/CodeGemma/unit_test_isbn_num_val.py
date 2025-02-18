import unittest

class TestISBNValidator(unittest.TestCase):

    def test_valid_ISBN10(self):
        self.assertTrue(valid_ISBN('0307474285'))
        self.assertTrue(valid_ISBN('0-307-47428-0'))

    def test_invalid_ISBN10(self):
        self.assertFalse(valid_ISBN('0307474286'))
        self.assertFalse(valid_ISBN('0-307-47428-1'))

    def test_valid_ISBN13(self):
        self.assertTrue(valid_ISBN('9780307474284'))
        self.assertTrue(valid_ISBN('978-0-307-47428-0'))

    def test_invalid_ISBN13(self):
        self.assertFalse(valid_ISBN('9780307474285'))
        self.assertFalse(valid_ISBN('978-0-307-47428-1'))

    def test_validate_isbn(self):
        self.assertEqual(validate_isbn('0307474285'), 'Valid ISBN number.')
        self.assertEqual(validate_isbn('9780307474284'), 'Valid ISBN number.')
        self.assertEqual(validate_isbn('0307474286'), 'Invalid ISBN number.')
        self.assertEqual(validate_isbn('9780307474285'), 'Invalid ISBN number.')

if __name__ == '__main__':
    unittest.main()