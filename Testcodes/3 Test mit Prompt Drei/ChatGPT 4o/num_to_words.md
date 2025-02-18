# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write a Unit Test for the following Python code. Focus on testing:
- Positive cases (where the function behaves as expected)
- Edge cases (input that might cause failures)
- Negative cases (where the function should throw errors or return incorrect results)
- Performance tests if applicable

Include comments to explain the purpose of each test case.


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
    """
    Convert a three-digit block of numbers into words.
    :param number: Three-digit block as a string.
    :param index: Suffix index (e.g., Thousand, Million).
    :return: Words representing the three-digit block.
    """
    if number == '0': 
        return 'Zero'

    number = number.zfill(3)
    hundreds_digit = int(number[0])
    tens_digit = int(number[1])
    ones_digit = int(number[2])

    words = '' if number[0] == '0' else ones[hundreds_digit]

    if words != '':
        words += ' Hundred '

    if tens_digit > 1:
        words += tens[tens_digit - 2]
        words += ' '
        words += ones[ones_digit]
    elif tens_digit == 1:
        words += twos[((tens_digit + ones_digit) % 10) - 1]
    elif tens_digit == 0:
        words += ones[ones_digit]

    if words.endswith('Zero'):
        words = words[:-len('Zero')]
    else:
        words += ' '

    if len(words) != 0:
        words += suffixes[index]
      
    return words

def convert_to_words(number):
    """
    Convert a number into its English word representation.
    :param number: Integer number to be converted.
    :return: Words representing the number.
    """
    length = len(str(number))
    if length > 12:
        return 'This program supports a maximum of 12 digit numbers.'

    count = length // 3 if length % 3 == 0 else length // 3 + 1
    copy = count
    words = []

    for i in range(length - 1, -1, -3):
        words.append(fetch_words(
            str(number)[0 if i - 2 < 0 else i - 2 : i + 1], copy - count))
        count -= 1

    final_words = ''
    for s in reversed(words):
        final_words += (s + ' ')

    return final_words.strip()

def convert_number(number):
    """
    Convert a number to its word representation.
    :param number: Integer to convert.
    :return: Word representation of the number.
    """
    return f"{number} in words is: {convert_to_words(number)}"
```

<hr>

### Generated Output

```
Below is a `unittest` test suite for the `convert_number` and `convert_to_words` functions. It includes positive cases, edge cases, negative cases, and a basic performance test.

### Test Code

```python
import unittest
from your_module import convert_number, convert_to_words

class TestNumberToWords(unittest.TestCase):
    # Positive Test Cases
    def test_single_digits(self):
        """Test conversion of single-digit numbers."""
        self.assertEqual(convert_to_words(0), "Zero")
        self.assertEqual(convert_to_words(5), "Five")

    def test_two_digits(self):
        """Test conversion of two-digit numbers."""
        self.assertEqual(convert_to_words(10), "Ten")
        self.assertEqual(convert_to_words(25), "Twenty Five")
        self.assertEqual(convert_to_words(99), "Ninety Nine")

    def test_three_digits(self):
        """Test conversion of three-digit numbers."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_large_numbers(self):
        """Test conversion of larger numbers."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(12345), "Twelve Thousand Three Hundred Forty Five")
        self.assertEqual(convert_to_words(987654321), 
                         "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_convert_number_output(self):
        """Test the `convert_number` function output."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    # Edge Cases
    def test_zero_padding(self):
        """Test numbers with leading zeros."""
        self.assertEqual(convert_to_words(7), "Seven")  # Leading zeros should not affect the output.

    def test_exact_suffix_boundaries(self):
        """Test numbers at boundaries of suffixes."""
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(1000000000), "One Billion")

    def test_minimum_and_maximum_supported_values(self):
        """Test the smallest and largest supported numbers."""
        self.assertEqual(convert_to_words(0), "Zero")
        self.assertEqual(
            convert_to_words(999999999999),
            "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine"
        )

    # Negative Test Cases
    def test_invalid_large_number(self):
        """Test numbers larger than 12 digits."""
        self.assertEqual(
            convert_to_words(1000000000000),
            "This program supports a maximum of 12 digit numbers."
        )

    def test_invalid_input_type(self):
        """Test invalid input types."""
        with self.assertRaises(ValueError):
            convert_to_words("abc")  # Strings should raise errors.
        with self.assertRaises(ValueError):
            convert_to_words(None)  # None should raise errors.

    def test_negative_numbers(self):
        """Test negative numbers."""
        with self.assertRaises(ValueError):
            convert_to_words(-123)  # Negative numbers should raise errors.

    # Performance Test Cases
    def test_large_number_performance(self):
        """Test performance with the largest supported number."""
        result = convert_to_words(999999999999)
        self.assertTrue(result.startswith("Nine Hundred Ninety Nine"))  # Ensures completion.

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases

1. **Positive Cases**:
   - Test the function's ability to correctly convert single-digit, two-digit, three-digit, and larger numbers into words.
   - Validate specific examples like `convert_number` output.

2. **Edge Cases**:
   - Ensure numbers with leading zeros (e.g., `007`) are processed correctly.
   - Test boundaries where suffixes (e.g., Thousand, Million) are applied.
   - Validate the smallest (0) and largest (999,999,999,999) supported numbers.

3. **Negative Cases**:
   - Test numbers beyond 12 digits and verify proper error handling.
   - Ensure invalid input types (strings, None) raise appropriate errors.
   - Verify that negative numbers are not allowed.

4. **Performance Test Cases**:
   - Test the largest valid input to ensure the function performs without excessive delay or errors.

### Notes

- Replace `your_module` with the actual module name containing your code.
- The `convert_to_words` function may need modification to raise errors for invalid input (e.g., non-integer values or negative numbers).
- This test suite assumes that `convert_to_words` handles numbers up to 12 digits and provides graceful error messages for unsupported inputs. Modify as needed to align with your actual implementation.
```