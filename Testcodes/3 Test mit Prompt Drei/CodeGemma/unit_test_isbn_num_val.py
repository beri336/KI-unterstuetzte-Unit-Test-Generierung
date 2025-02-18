import unittest

class TestValidISBN(unittest.TestCase):

    # Positive cases
    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN('0307950358'))

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN('9780307950359'))

    # Edge cases
    def test_isbn_with_hyphens(self):
        self.assertTrue(valid_ISBN('978-0307950359'))

    def test_isbn_with_spaces(self):
        self.assertTrue(valid_ISBN('978 0307950359'))

    # Negative cases
    def test_invalid_isbn_length(self):
        self.assertFalse(valid_ISBN('123456789'))

    def test_invalid_isbn10_format(self):
        self.assertFalse(valid_ISBN('a307950358'))

    def test_invalid_isbn13_format(self):
        self.assertFalse(valid_ISBN('abcdefghijkl'))

    # Performance tests
    def test_performance(self):
        import timeit
        isbn = '9780307950359'
        number_of_iterations = 10000
        start_time = timeit.default_timer()
        for _ in range(number_of_iterations):
            valid_ISBN(isbn)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        self.assertLess(elapsed_time, 1)

if __name__ == '__main__':
    unittest.main()