import unittest

ones = (
   'Zero', 'One', 'Two', 'Three', 'Four',
   'Five', 'Six', 'Seven', 'Eight', 'Nine'
)

twos = (
   'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
   'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'
)

tens = (
   'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty',
   'Seventy', 'Eighty', 'Ninety', 'Hundred'
)

suffixes = (
   '', 'Thousand', 'Million', 'Billion'
)

def fetch_words(number, index):
    # ... function implementation ...

def convert_to_words(number):
    # ... function implementation ...

def convert_number(number):
    # ... function implementation ...


class TestNumberConversion(unittest.TestCase):

    def test_positive_cases(self):
        """Test positive cases with expected results."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three Thousand")
        self.assertEqual(convert_number(1000), "1000 in words is: One Thousand")
        self.assertEqual(convert_number(1234567), "1234567 in words is: One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven ")

    def test_edge_cases(self):
        """Test edge cases like zero and numbers at the limits."""
        self.assertEqual(convert_number(0), "0 in words is: Zero")
        self.assertEqual(convert_number(999), "999 in words is: Nine Hundred Ninety Nine ")
        # Test cases for numbers near the maximum supported length (12 digits)

    def test_negative_cases(self):
        """Test cases that should raise errors or return incorrect results."""
        with self.assertRaises(ValueError):
            convert_number(1000000000000)  # Number exceeds maximum length 

    def test_performance(self):
        """Performance tests (optional). Use benchmarks to measure time taken for conversion."""
        numbers = [123, 1234567, 999999999]
        for number in numbers:
            start_time = time.time()  # Record start time
            convert_to_words(number)  # Perform conversion
            end_time = time.time()   # Record end time
            print(f"Time taken for {number}: {end_time - start_time:.4f} seconds")



if __name__ == '__main__':
    unittest.main() 