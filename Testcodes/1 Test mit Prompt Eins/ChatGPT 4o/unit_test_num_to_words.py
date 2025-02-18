import unittest
from your_module import fetch_words, convert_to_words, convert_number

class TestNumberToWords(unittest.TestCase):

    def test_fetch_words(self):
        """Test the fetch_words function with various inputs."""
        self.assertEqual(fetch_words('123', 1), 'One Hundred Twenty Three Thousand', "Should convert '123' correctly.")
        self.assertEqual(fetch_words('045', 0), 'Forty Five', "Should convert '045' correctly without a suffix.")
        self.assertEqual(fetch_words('009', 2), 'Nine Million', "Should handle leading zeros correctly.")
        self.assertEqual(fetch_words('000', 0), 'Zero', "Should return 'Zero' for all zeros block.")
        self.assertEqual(fetch_words('700', 3), 'Seven Hundred Billion', "Should convert hundreds correctly with suffix.")

    def test_convert_to_words(self):
        """Test the convert_to_words function with complete numbers."""
        self.assertEqual(convert_to_words(123456789), "One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine", "Should convert 123456789 correctly.")
        self.assertEqual(convert_to_words(1001), "One Thousand One", "Should handle numbers with skipped tens digit.")
        self.assertEqual(convert_to_words(0), "Zero", "Should return 'Zero' for 0.")
        self.assertEqual(convert_to_words(1000000), "One Million", "Should handle large round numbers.")
        self.assertEqual(convert_to_words(1000000000), "One Billion", "Should handle exactly one billion.")
        self.assertEqual(convert_to_words(12), "Twelve", "Should handle numbers less than 20.")
        self.assertEqual(convert_to_words(987654321), "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One", "Should convert 987654321 correctly.")

    def test_convert_number(self):
        """Test the convert_number function to ensure correct formatting."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three", "Should return correct sentence for 123.")
        self.assertEqual(convert_number(4567), "4567 in words is: Four Thousand Five Hundred Sixty Seven", "Should return correct sentence for 4567.")
        self.assertEqual(convert_number(0), "0 in words is: Zero", "Should return correct sentence for 0.")
        self.assertEqual(convert_number(1000000), "1000000 in words is: One Million", "Should return correct sentence for 1,000,000.")
        self.assertEqual(convert_number(1000000000000), "1000000000000 in words is: This program supports a maximum of 12 digit numbers.", "Should enforce the 12-digit limit.")

if __name__ == '__main__':
    unittest.main()