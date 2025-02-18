import unittest

from main import convert_number, convert_to_words, fetch_words

class TestNumberConversion(unittest.TestCase):

    def test_convert_number_positive_integer(self):
        """Test converting a positive integer to words."""
        result = convert_number(1234567)
        expected = "1234567 in words is: One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
        self.assertEqual(result, expected)

    def test_convert_number_zero(self):
        """Test converting zero to words."""
        result = convert_number(0)
        expected = "0 in words is: Zero"
        self.assertEqual(result, expected)

    def test_convert_number_negative_integer(self):
        """Test converting a negative integer to words."""
        result = convert_number(-1234567)
        expected = "-1234567 in words is: Negative One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
        self.assertEqual(result, expected)

    def test_convert_number_edge_case(self):
        """Test converting an integer near the maximum supported length."""
        result = convert_number(9999999999)
        expected = "9999999999 in words is: Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine"
        self.assertEqual(result, expected)

    def test_convert_number_error_handling(self):
        """Test handling an integer larger than the supported maximum."""
        with self.assertRaises(ValueError):
            convert_number(100000000000)  

    def test_fetch_words_zero(self):
        """Test converting '0' to words."""
        result = fetch_words('0', 0)
        expected = 'Zero'
        self.assertEqual(result, expected)

    def test_fetch_words_hundred(self):
        """Test converting a three-digit number with a hundreds digit."""
        result = fetch_words('123', 0)
        expected = 'One Hundred Twenty Three'
        self.assertEqual(result, expected)

    def test_fetch_words_tens_only(self):
        """Test converting a three-digit number with only tens and ones digits."""
        result = fetch_words('034', 0)
        expected = 'Thirty Four'
        self.assertEqual(result, expected)

    def test_fetch_words_tens_and_ones(self):
        """Test converting a three-digit number with tens and ones digits."""
        result = fetch_words('215', 0)
        expected = 'Two Hundred Fifteen'
        self.assertEqual(result, expected)

    def test_fetch_words_suffix(self):
        """Test adding the suffix to the word representation."""
        result = fetch_words('100', 2)  # Adding "Million" suffix
        expected = 'One Hundred Thousand Million'
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()