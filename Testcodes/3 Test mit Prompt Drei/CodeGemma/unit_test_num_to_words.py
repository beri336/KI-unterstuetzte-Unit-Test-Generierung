import unittest

class TestNumberConversion(unittest.TestCase):

    # Positive cases
    def test_positive_numbers(self):
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")
        self.assertEqual(convert_number(456), "456 in words is: Four Hundred Fifty Six")

    # Edge cases
    def test_zero(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")

    def test_long_numbers(self):
        self.assertEqual(convert_number(123456789), "123456789 in words is: One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine")

    # Negative cases
    def test_invalid_input(self):
        with self.assertRaises(Exception):
            convert_number('abc')

    # Performance tests
    def test_performance(self):
        import timeit
        number = 123456789
        num_runs = 1000
        start_time = timeit.default_timer()
        for _ in range(num_runs):
            convert_number(number)
        end_time = timeit.default_timer()
        self.assertLess(end_time - start_time, 1)

if __name__ == '__main__':
    unittest.main()