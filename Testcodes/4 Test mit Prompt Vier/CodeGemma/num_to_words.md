# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: CodeGemma:7b

<hr>

### Prompt

```
Write me a Unit Test for the following Python code. Break the process into multiple tests:

- One function per test case.
- Each test should have a clear and descriptive name indicating what it tests (e.g., `test_function_name_valid_input`, `test_function_name_edge_case`, etc.)
- Include normal cases, edge cases, and cases that should raise exceptions.
- Add comments to each test cases.
Write the test functions step by step, explaining each part before moving on.
filename: "main.py"

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
```python
import unittest

class TestFetchWords(unittest.TestCase):

    def test_fetch_words_zero(self):
        self.assertEqual(fetch_words('000', 0), 'Zero')

    def test_fetch_words_one_hundred(self):
        self.assertEqual(fetch_words('001', 0), 'One Hundred')

    def test_fetch_words_twenty_three(self):
        self.assertEqual(fetch_words('023', 0), 'Twenty Three')

    def test_fetch_words_exception(self):
        with self.assertRaises(ValueError):
            fetch_words('abc', 0)


class TestConvertToWords(unittest.TestCase):

    def test_convert_to_words_four_digits(self):
        self.assertEqual(convert_to_words(1234), 'One Thousand Two Hundred Thirty Four')

    def test_convert_to_words_ten_digits(self):
        self.assertEqual(convert_to_words(1234567890), 'One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety')

    def test_convert_to_words_exception(self):
        with self.assertRaises(ValueError):
            convert_to_words('abc')


class TestConvertNumber(unittest.TestCase):

    def test_convert_number_to_words(self):
        self.assertEqual(convert_number(1234), '1234 in words is: One Thousand Two Hundred Thirty Four')

    def test_convert_number_to_words_exception(self):
        with self.assertRaises(ValueError):
            convert_number('abc')
```
```