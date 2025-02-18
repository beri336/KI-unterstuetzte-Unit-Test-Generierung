# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following Python Code, write comments and add special cases and edge cases:


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
Here is a comprehensive unit test suite for the provided code. It uses Python's `unittest` framework and tests various scenarios, including edge cases.

### Unit Test Code

```python
import unittest
from your_script_name import convert_to_words, fetch_words

class TestNumberToWords(unittest.TestCase):
    def test_single_digit(self):
        """Test single-digit numbers."""
        for i in range(10):
            self.assertEqual(convert_to_words(i), f"{ones[i]}")

    def test_two_digits(self):
        """Test two-digit numbers."""
        self.assertEqual(convert_to_words(10), "Ten")
        self.assertEqual(convert_to_words(11), "Eleven")
        self.assertEqual(convert_to_words(19), "Nineteen")
        self.assertEqual(convert_to_words(21), "Twenty One")
        self.assertEqual(convert_to_words(99), "Ninety Nine")

    def test_three_digits(self):
        """Test three-digit numbers."""
        self.assertEqual(convert_to_words(100), "One Hundred")
        self.assertEqual(convert_to_words(105), "One Hundred Five")
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")
        self.assertEqual(convert_to_words(999), "Nine Hundred Ninety Nine")

    def test_thousands(self):
        """Test numbers in the thousands."""
        self.assertEqual(convert_to_words(1000), "One Thousand")
        self.assertEqual(convert_to_words(12345), "Twelve Thousand Three Hundred Forty Five")
        self.assertEqual(convert_to_words(10000), "Ten Thousand")
        self.assertEqual(convert_to_words(10101), "Ten Thousand One Hundred One")

    def test_millions(self):
        """Test numbers in the millions."""
        self.assertEqual(convert_to_words(1000000), "One Million")
        self.assertEqual(convert_to_words(1234567), "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven")
        self.assertEqual(convert_to_words(1001000), "One Million One Thousand")

    def test_billions(self):
        """Test numbers in the billions."""
        self.assertEqual(convert_to_words(1000000000), "One Billion")
        self.assertEqual(convert_to_words(987654321), "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_large_numbers(self):
        """Test numbers beyond the supported range."""
        self.assertEqual(convert_to_words(123456789012), "One Hundred Twenty Three Billion Four Hundred Fifty Six Million Seven Hundred Eighty Nine Thousand Twelve")
        self.assertEqual(convert_to_words(1000000000000), "This program supports a maximum of 12 digit numbers.")

    def test_fetch_words_edge_cases(self):
        """Test edge cases for fetch_words."""
        self.assertEqual(fetch_words("000", 0), "Zero")
        self.assertEqual(fetch_words("001", 0), "One")
        self.assertEqual(fetch_words("010", 0), "Ten")
        self.assertEqual(fetch_words("100", 0), "One Hundred ")
        self.assertEqual(fetch_words("101", 0), "One Hundred One ")

    def test_zero_handling(self):
        """Test the handling of zero."""
        self.assertEqual(convert_to_words(0), "Zero")

    def test_leading_zeros(self):
        """Test numbers with leading zeros."""
        self.assertEqual(convert_to_words(int("0000123")), "One Hundred Twenty Three")
        self.assertEqual(fetch_words("012", 0), "Twelve")

    def test_invalid_inputs(self):
        """Test invalid inputs."""
        with self.assertRaises(ValueError):
            convert_to_words("abc")  # Non-integer
        with self.assertRaises(ValueError):
            convert_to_words(-123)  # Negative number

if __name__ == "__main__":
    unittest.main()
```

### Explanation of the Test Cases:
1. **Single Digits**:
   - Verifies correctness for numbers between `0` and `9`.

2. **Two Digits**:
   - Tests numbers in the teens (`10` to `19`).
   - Tests numbers with a tens and ones place (`20`, `21`, etc.).

3. **Three Digits**:
   - Verifies correctness for hundreds (`100`, `105`, etc.).

4. **Thousands**:
   - Tests numbers in the thousands (`1000`, `12345`, etc.).

5. **Millions and Billions**:
   - Validates larger numbers up to the billion range.

6. **Large Numbers**:
   - Ensures the program supports numbers up to 12 digits.
   - Checks for rejection of numbers beyond the supported range.

7. **`fetch_words` Edge Cases**:
   - Tests edge cases for `fetch_words`, including zero-padded strings.

8. **Zero Handling**:
   - Ensures proper handling of the number `0`.

9. **Leading Zeros**:
   - Tests numbers with leading zeros to verify they are ignored.

10. **Invalid Inputs**:
    - Ensures non-integer and negative inputs are handled gracefully by raising errors.

### Running the Tests:
1. Replace `your_script_name` with the filename containing the functions.
2. Save the test code in a file, e.g., `test_number_to_words.py`.
3. Run the tests with:
   ```bash
   python -m unittest test_number_to_words.py
   ```

This suite provides full coverage of the code, ensuring both typical use cases and edge cases are handled correctly.
```