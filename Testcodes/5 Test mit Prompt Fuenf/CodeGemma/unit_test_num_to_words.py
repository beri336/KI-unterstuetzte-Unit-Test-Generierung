import unittest

from main import convert_number, convert_to_words

class TestNumberConversion(unittest.TestCase):

    # Test normal input cases with common values.
    def test_common_values(self):
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")
        self.assertEqual(convert_number(456), "456 in words is: Four Hundred Fifty Six")
        self.assertEqual(convert_number(789), "789 in words is: Seven Hundred Eighty Nine")

    # Test edge cases.
    def test_edge_cases(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")
        self.assertEqual(convert_number(100), "100 in words is: One Hundred")
        self.assertEqual(convert_number(1000), "1000 in words is: One Thousand")

    # Test invalid input cases that should raise exceptions.
    def test_invalid_input(self):
        with self.assertRaises(Exception):
            convert_number(-123)

        with self.assertRaises(Exception):
            convert_number(1234567890123)

if __name__ == '__main__':
    unittest.main()