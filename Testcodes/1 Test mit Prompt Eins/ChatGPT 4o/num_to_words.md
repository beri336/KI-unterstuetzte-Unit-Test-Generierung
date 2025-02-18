# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following given Python Code:

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
Here’s a `unittest`-based test suite for the provided code. This will verify the correctness of the functions `fetch_words`, `convert_to_words`, and `convert_number`.

```python
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
```

### Explanation of Test Cases:

1. **`test_fetch_words`**:
   - Verifies the conversion of individual three-digit blocks.
   - Handles leading zeros, suffixes (e.g., "Thousand", "Million"), and edge cases like all zeros.

2. **`test_convert_to_words`**:
   - Tests full number conversions, including:
     - Large numbers with multiple blocks.
     - Small numbers and single-digit edge cases.
     - Special cases like numbers under 20 and exact multiples of 10 or powers of 10.

3. **`test_convert_number`**:
   - Ensures the correct format is applied by `convert_number`, including the "in words is:" prefix.
   - Checks for the 12-digit number limit.

### Usage:
1. Replace `your_module` with the actual file name where the code resides.
2. Save the test suite in a separate file, e.g., `test_number_to_words.py`.
3. Run it using:
   ```bash
   python -m unittest test_number_to_words.py
   ```
```