# Unit Test Documentation
## Original File: ../ISBN-Validator/isbn_num_val.py

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
filename: "isbn_num_val.py"

def valid_ISBN(isbn):
    """
    Check if the entered number is a valid ISBN-10 or ISBN-13.
    :param isbn: The ISBN number as a string.
    :return: True if valid, False otherwise.
    """
    # Remove hyphens and spaces from the ISBN
    isbn = isbn.replace('-', '').replace(' ', '')

    # Check if the length of the ISBN is valid
    if len(isbn) == 10:
        return valid_ISBN10(isbn)
    elif len(isbn) == 13:
        return valid_ISBN13(isbn)
    else:
        return False

def valid_ISBN10(isbn):
    """
    Check if the entered number is a valid 10-digit ISBN.
    :param isbn: The ISBN-10 number as a string.
    :return: True if valid, False otherwise.
    """
    # Validate format of the ISBN-10
    if not isbn[:-1].isdigit() or not isbn[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']:
        return False

    # Calculate the check digit
    check_digit = 0
    weight = 10
    for digit in isbn[:-1]:
        check_digit += int(digit) * weight
        weight -= 1

    check_digit %= 11
    if isbn[-1] == 'X':
        return check_digit == 10
    return str(check_digit) == isbn[-1]

def valid_ISBN13(isbn):
    """
    Check if the entered number is a valid 13-digit ISBN.
    :param isbn: The ISBN-13 number as a string.
    :return: True if valid, False otherwise.
    """
    # Validate format of the ISBN-13
    if not isbn.isdigit():
        return False

    # Calculate the check digit
    check_digit = 0
    weight = [1, 3] * 6
    for digit, w in zip(isbn[:-1], weight):
        check_digit += int(digit) * w

    check_digit %= 10
    check_digit = (10 - check_digit) % 10

    return str(check_digit) == isbn[-1]

def validate_isbn(isbn):
    """
    Validate an ISBN.
    :param isbn: The ISBN number as a string.
    :return: "Valid ISBN number." or "Invalid ISBN number."
    """
    if valid_ISBN(isbn):
        return "Valid ISBN number."
    else:
        return "Invalid ISBN number."
```

<hr>

### Generated Output

```
Here’s how to write unit tests for the `isbn_num_val.py` file, breaking down the process into multiple tests for each function. We’ll use the `unittest` framework in Python.

---

### Step 1: Setting up the test file
Create a new file `test_isbn_num_val.py` with the following structure:

```python
import unittest
from isbn_num_val import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):
    pass
```

This sets up the testing framework.

---

### Step 2: Write tests for `valid_ISBN`

#### Explanation:
- Test normal cases (valid ISBN-10 and ISBN-13).
- Test edge cases (invalid length, invalid characters).

```python
class TestISBNValidation(unittest.TestCase):
    def test_valid_ISBN_valid_ISBN10(self):
        # Test a valid ISBN-10
        self.assertTrue(valid_ISBN("0471958697"))

    def test_valid_ISBN_valid_ISBN13(self):
        # Test a valid ISBN-13
        self.assertTrue(valid_ISBN("9780470059029"))

    def test_valid_ISBN_invalid_length(self):
        # Test an ISBN with invalid length
        self.assertFalse(valid_ISBN("123456789"))

    def test_valid_ISBN_invalid_characters(self):
        # Test an ISBN with invalid characters
        self.assertFalse(valid_ISBN("ISBN123456X"))
```

---

### Step 3: Write tests for `valid_ISBN10`

#### Explanation:
- Test normal cases (valid and invalid ISBN-10).
- Test edge cases (invalid check digit, special 'X' as check digit).

```python
class TestISBNValidation(unittest.TestCase):
    def test_valid_ISBN10_valid(self):
        # Test a valid ISBN-10
        self.assertTrue(valid_ISBN10("0471958697"))

    def test_valid_ISBN10_invalid_check_digit(self):
        # Test an ISBN-10 with incorrect check digit
        self.assertFalse(valid_ISBN10("0471958696"))

    def test_valid_ISBN10_invalid_format(self):
        # Test an ISBN-10 with invalid characters
        self.assertFalse(valid_ISBN10("04719A8697"))

    def test_valid_ISBN10_check_digit_X(self):
        # Test an ISBN-10 with 'X' as the check digit
        self.assertTrue(valid_ISBN10("0306406152"))
```

---

### Step 4: Write tests for `valid_ISBN13`

#### Explanation:
- Test normal cases (valid and invalid ISBN-13).
- Test edge cases (invalid check digit, non-digit characters).

```python
class TestISBNValidation(unittest.TestCase):
    def test_valid_ISBN13_valid(self):
        # Test a valid ISBN-13
        self.assertTrue(valid_ISBN13("9780470059029"))

    def test_valid_ISBN13_invalid_check_digit(self):
        # Test an ISBN-13 with incorrect check digit
        self.assertFalse(valid_ISBN13("9780470059028"))

    def test_valid_ISBN13_invalid_format(self):
        # Test an ISBN-13 with non-digit characters
        self.assertFalse(valid_ISBN13("97804700A9029"))
```

---

### Step 5: Write tests for `validate_isbn`

#### Explanation:
- Test cases for the final validation function.
- Combine results from `valid_ISBN`.

```python
class TestISBNValidation(unittest.TestCase):
    def test_validate_isbn_valid_ISBN10(self):
        # Test a valid ISBN-10
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")

    def test_validate_isbn_valid_ISBN13(self):
        # Test a valid ISBN-13
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")

    def test_validate_isbn_invalid(self):
        # Test an invalid ISBN
        self.assertEqual(validate_isbn("1234567890"), "Invalid ISBN number.")
```

---

### Step 6: Run all tests
To run the tests, execute the following command:

```bash
python -m unittest test_isbn_num_val.py
```

---

### Full Test File

```python
import unittest
from isbn_num_val import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):
    # Tests for valid_ISBN
    def test_valid_ISBN_valid_ISBN10(self):
        self.assertTrue(valid_ISBN("0471958697"))

    def test_valid_ISBN_valid_ISBN13(self):
        self.assertTrue(valid_ISBN("9780470059029"))

    def test_valid_ISBN_invalid_length(self):
        self.assertFalse(valid_ISBN("123456789"))

    def test_valid_ISBN_invalid_characters(self):
        self.assertFalse(valid_ISBN("ISBN123456X"))

    # Tests for valid_ISBN10
    def test_valid_ISBN10_valid(self):
        self.assertTrue(valid_ISBN10("0471958697"))

    def test_valid_ISBN10_invalid_check_digit(self):
        self.assertFalse(valid_ISBN10("0471958696"))

    def test_valid_ISBN10_invalid_format(self):
        self.assertFalse(valid_ISBN10("04719A8697"))

    def test_valid_ISBN10_check_digit_X(self):
        self.assertTrue(valid_ISBN10("0306406152"))

    # Tests for valid_ISBN13
    def test_valid_ISBN13_valid(self):
        self.assertTrue(valid_ISBN13("9780470059029"))

    def test_valid_ISBN13_invalid_check_digit(self):
        self.assertFalse(valid_ISBN13("9780470059028"))

    def test_valid_ISBN13_invalid_format(self):
        self.assertFalse(valid_ISBN13("97804700A9029"))

    # Tests for validate_isbn
    def test_validate_isbn_valid_ISBN10(self):
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")

    def test_validate_isbn_valid_ISBN13(self):
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")

    def test_validate_isbn_invalid(self):
        self.assertEqual(validate_isbn("1234567890"), "Invalid ISBN number.")
```

This test suite ensures that all edge cases and normal scenarios are covered for the ISBN validation logic.
```