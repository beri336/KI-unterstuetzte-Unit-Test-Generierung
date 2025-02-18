# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "number_to_words.py"


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
Below is the `unittest` test suite for the provided `number_to_words.py` module. It includes test cases for normal inputs, edge cases, and invalid input handling.

### Test Suite

```python
import unittest
from number_to_words import convert_to_words, convert_number, fetch_words


class TestNumberToWords(unittest.TestCase):

    # Normal Input Cases
    def test_single_digit(self):
        """Test single-digit numbers."""
        self.assertEqual(convert_to_words(5), "Five")
        self.assertEqual(convert_to_words(0), "Zero")

    def test_two_digits(self):
        """Test two-digit numbers."""
        self.assertEqual(convert_to_words(15), "Fifteen")
        self.assertEqual(convert_to_words(45), "Forty Five")

    def test_three_digits(self):
        """Test three-digit numbers."""
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(900), "Nine Hundred")

    def test_large_numbers(self):
        """Test large numbers with thousands, millions, and billions."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(123456789), 
                         "One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine")

    def test_convert_number_function(self):
        """Test the convert_number function."""
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    # Edge Cases
    def test_zero(self):
        """Test the number zero."""
        self.assertEqual(convert_to_words(0), "Zero")

    def test_hundred_boundary(self):
        """Test numbers at the boundary of hundreds."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_thousand_boundary(self):
        """Test numbers at the boundary of thousands."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(1999), "One Thousand Nine Hundred Ninety Nine")

    def test_maximum_supported_number(self):
        """Test the maximum supported number (12 digits)."""
        self.assertEqual(convert_to_words(999999999999), 
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_exceeding_max_digits(self):
        """Test numbers exceeding the maximum supported digits."""
        self.assertEqual(convert_to_words(1000000000000), 
                         "This program supports a maximum of 12 digit numbers.")

    def test_fetch_words_function(self):
        """Test the fetch_words function with three-digit blocks."""
        self.assertEqual(fetch_words("123", 0), "One Hundred Twenty Three ")
        self.assertEqual(fetch_words("007", 0), "Seven ")
        self.assertEqual(fetch_words("500", 1), "Five Hundred Thousand")

    # Invalid Input Cases
    def test_negative_number(self):
        """Test with a negative number."""
        with self.assertRaises(ValueError):
            convert_to_words(-123)

    def test_non_integer_input(self):
        """Test with non-integer inputs."""
        with self.assertRaises(ValueError):
            convert_to_words("123")

    def test_empty_input(self):
        """Test with empty input."""
        with self.assertRaises(TypeError):  # Expected since the function expects an integer
            convert_to_words()

    def test_large_number_boundary(self):
        """Test exactly 12-digit number to ensure it works."""
        self.assertEqual(convert_to_words(999999999999), 
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases

1. **Normal Input Cases**:
   - Test the function with standard numbers, including single, two, three, and large numbers.
   - Verify that both `convert_to_words` and `convert_number` return expected outputs.

2. **Edge Cases**:
   - Cover boundary values, such as 0, 100, 1000, and the maximum 12-digit number.
   - Test the response when exceeding the maximum supported digits.

3. **Invalid Input Cases**:
   - Test with negative numbers, non-integer inputs, and empty input.
   - Ensure proper exceptions are raised and handled.

This suite ensures that the code works correctly across a wide range of valid, edge, and invalid inputs.
```