import unittest
from your_module import fetch_words, convert_to_words  # Import functions to test

class TestEnglishNumberConverter(unittest.TestCase):

    def setUp(self):
        self.ones = (
            'Zero', 'One', 'Two', 'Three', 'Four',
            'Five', 'Six', 'Seven', 'Eight', 'Nine'
        )
        self.twos = (
            'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
            'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'
        )
        self.tens = (
            'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty',
            'Seventy', 'Eighty', 'Ninety', 'Hundred'
        )
        self.suffixes = (
            '', 'Thousand', 'Million', 'Billion'
        )

    def test_positive_cases(self):
        # Test conversion of positive numbers
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(123456789), "One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine")
        self.assertEqual(convert_number(10000), "Ten Thousand in words is: One Thousand")

    def test_edge_cases(self):
        # Test conversion of edge cases
        self.assertEqual(fetch_words('0', 2), 'Zero')
        self.assertEqual(fetch_words('100', 2), 'One Hundred')
        self.assertEqual(fetch_words('101', 1), 'One Hundred One')

    def test_negative_cases(self):
        # Test that the function throws an error for negative numbers
        with self.assertRaises(ValueError):
            convert_to_words(-123)

    def test_performance_tests(self):
        # Performance test: Measure conversion time of large numbers
        import timeit

        start_time = timeit.default_timer()
        convert_to_words(1000000000)
        end_time = timeit.default_timer()

        print(f"Conversion time for 1 billion: {end_time - start_time} seconds")

    def test_invalid_input(self):
        # Test that the function throws an error for invalid input
        with self.assertRaises(ValueError):
            convert_to_words('abc')

if __name__ == '__main__':
    unittest.main()