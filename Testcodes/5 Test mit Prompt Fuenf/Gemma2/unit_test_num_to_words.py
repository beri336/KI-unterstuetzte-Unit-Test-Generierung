import unittest

from main import convert_number  # Import your function


class TestConvertNumber(unittest.TestCase):

    def test_normal_input(self):
        """Test normal input cases with common values."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")
        self.assertEqual(convert_number(1000), "1000 in words is: One Thousand")
        self.assertEqual(convert_number(999999), "999999 in words is: Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_edge_cases(self):
        """Test edge cases (e.g., empty lists, negative numbers). """
        self.assertEqual(convert_number(0), "0 in words is: Zero")
        self.assertEqual(convert_number(-123), "-123 in words is: Negative One Hundred Twenty Three")

    def test_invalid_input(self):
        """Test invalid input cases that should raise exceptions."""
        with self.assertRaises(TypeError):
            convert_number("abc")  # Input should be an integer


if __name__ == '__main__':
    unittest.main()