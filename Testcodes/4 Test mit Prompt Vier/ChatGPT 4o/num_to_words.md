# Unit Test Documentation
## Original File: ../Number-To-Words/num_to_words.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following Python code. Break the process into multiple tests:

- One function per test case.
- Each test should have a clear and descriptive name indicating what it tests (e.g., `test_function_name_valid_input`, `test_function_name_edge_case`, etc.)
- Include normal cases, edge cases, and cases that should raise exceptions.
- Add comments to each test cases.
Write the test functions step by step, explaining each part before moving on.
filename: "number_to_words.py"

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
Here’s a comprehensive unit test suite for the provided `number_to_words.py` module. Each function is tested separately with normal, edge, and exception cases where applicable.

---

### Step 1: Set Up the Test File
Create a test file named `test_number_to_words.py`.

```python
import unittest
from number_to_words import fetch_words, convert_to_words, convert_number

class TestNumberToWords(unittest.TestCase):
    pass
```

---

### Step 2: Write Tests for `fetch_words`

#### Explanation:
- Test normal three-digit numbers.
- Test edge cases like zero and single-digit numbers.

```python
class TestNumberToWords(unittest.TestCase):
    def test_fetch_words_normal_case(self):
        # Test fetching words for a normal three-digit number
        self.assertEqual(fetch_words("123", 0), "One Hundred Twenty Three ")

    def test_fetch_words_with_suffix(self):
        # Test fetching words with a suffix index
        self.assertEqual(fetch_words("001", 1), "One Thousand")

    def test_fetch_words_zero(self):
        # Test fetching words for zero
        self.assertEqual(fetch_words("000", 0), "Zero")

    def test_fetch_words_single_digit(self):
        # Test fetching words for a single-digit number
        self.assertEqual(fetch_words("7", 0), "Seven ")

    def test_fetch_words_two_digits(self):
        # Test fetching words for a two-digit number
        self.assertEqual(fetch_words("85", 0), "Eighty Five ")
```

---

### Step 3: Write Tests for `convert_to_words`

#### Explanation:
- Test conversion of small and large numbers.
- Test the edge case for the maximum supported number.

```python
class TestNumberToWords(unittest.TestCase):
    def test_convert_to_words_small_number(self):
        # Test conversion for a small number
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")

    def test_convert_to_words_large_number(self):
        # Test conversion for a large number
        self.assertEqual(convert_to_words(987654321), 
                         "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_convert_to_words_max_supported_digits(self):
        # Test conversion for the maximum supported number
        self.assertEqual(convert_to_words(999999999999),
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_convert_to_words_exceeding_max_digits(self):
        # Test conversion for a number exceeding the maximum supported digits
        self.assertEqual(convert_to_words(1000000000000),
                         "This program supports a maximum of 12 digit numbers.")
```

---

### Step 4: Write Tests for `convert_number`

#### Explanation:
- Validate that the `convert_number` function formats the output correctly.

```python
class TestNumberToWords(unittest.TestCase):
    def test_convert_number_small_number(self):
        # Test conversion for a small number
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    def test_convert_number_large_number(self):
        # Test conversion for a large number
        self.assertEqual(convert_number(10001), "10001 in words is: Ten Thousand One")

    def test_convert_number_zero(self):
        # Test conversion for zero
        self.assertEqual(convert_number(0), "0 in words is: Zero")
```

---

### Step 5: Full Test File

```python
import unittest
from number_to_words import fetch_words, convert_to_words, convert_number

class TestNumberToWords(unittest.TestCase):
    # Tests for fetch_words
    def test_fetch_words_normal_case(self):
        self.assertEqual(fetch_words("123", 0), "One Hundred Twenty Three ")

    def test_fetch_words_with_suffix(self):
        self.assertEqual(fetch_words("001", 1), "One Thousand")

    def test_fetch_words_zero(self):
        self.assertEqual(fetch_words("000", 0), "Zero")

    def test_fetch_words_single_digit(self):
        self.assertEqual(fetch_words("7", 0), "Seven ")

    def test_fetch_words_two_digits(self):
        self.assertEqual(fetch_words("85", 0), "Eighty Five ")

    # Tests for convert_to_words
    def test_convert_to_words_small_number(self):
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")

    def test_convert_to_words_large_number(self):
        self.assertEqual(convert_to_words(987654321), 
                         "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_convert_to_words_max_supported_digits(self):
        self.assertEqual(convert_to_words(999999999999),
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_convert_to_words_exceeding_max_digits(self):
        self.assertEqual(convert_to_words(1000000000000),
                         "This program supports a maximum of 12 digit numbers.")

    # Tests for convert_number
    def test_convert_number_small_number(self):
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    def test_convert_number_large_number(self):
        self.assertEqual(convert_number(10001), "10001 in words is: Ten Thousand One")

    def test_convert_number_zero(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")
```

---

### Step 6: Run the Tests
Run the tests with:

```bash
python -m unittest test_number_to_words.py
```

This test suite thoroughly verifies the functionality of the `number_to_words.py` module, including normal scenarios, edge cases, and formatting requirements.
```