# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: Gemma2:9b

<hr>

### Prompt

```
Write a Unit Test for the following Python code. Focus on testing:
- Positive cases (where the function behaves as expected)
- Edge cases (input that might cause failures)
- Negative cases (where the function should throw errors or return incorrect results)
- Performance tests if applicable

Include comments to explain the purpose of each test case.

import os
import sqlite3
from sqlite3 import Error


list_of_names = [] # Global list of names for validation

def create_database_file(db_file):
    """
    Create a new SQLite database file if it does not exist.
    
    :param db_file: Path to the database file.
    :return: Connection object or None if creation fails.
    """
    try:
        # Check if the database file exists
        if not os.path.exists(db_file):
            # Ensure the directory for the database file exists
            db_dir = os.path.dirname(db_file)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                print(f"Directory created: {db_dir}")
            
            # Create the database file by connecting to it
            with sqlite3.connect(db_file) as conn:
                print(f"Database file created: {db_file}")
                return conn
        else:
            # If the file exists, simply connect to it
            with sqlite3.connect(db_file) as conn:
                print(f"Database file already exists: {db_file}")
                return conn
    except Error as e:
        print(f"Error creating the database file: {e}")
        return None

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        r_set = conn.execute('''SELECT * FROM tasks''')
        global list_of_names
        list_of_names = [student[1] for student in r_set]
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_task(conn, name, number):
    """Add a new task (contact) to the address book."""
    if name in list_of_names:
        return f"Error: {name} already exists."

    if not name or not number or len(number) != 10:
        return "Error: Name cannot be empty, and phone number must be 10 digits."

    sql = '''INSERT INTO tasks(name, status_id) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (name, number))
    conn.commit()
    list_of_names.append(name)
    return f"{name} added successfully."

def update_task(conn, name, number):
    """Update the phone number of an existing task."""
    if name not in list_of_names:
        return f"Error: {name} not found."

    sql = '''UPDATE tasks SET status_id = ? WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, (number, name))
    conn.commit()
    return f"{name} updated successfully."

def delete_task(conn, name):
    """Delete a task by name."""
    if name not in list_of_names:
        return f"Error: {name} not found."

    sql = 'DELETE FROM tasks WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))
    conn.commit()
    list_of_names.remove(name)
    return f"{name} deleted successfully."

def view_task_by_name(conn, name):
    """Query a task by name."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE name=?", (name,))
    rows = cur.fetchall()
    if not rows:
        return f"Error: {name} not found."
    return rows

def view_all_tasks(conn):
    """Get all rows in the tasks table."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return rows

def reset_all_tasks(conn):
    """Delete all entries in the database."""
    try:
        sql = "DELETE FROM tasks"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        global list_of_names
        list_of_names = [] # Reset the global list of names
        return "All entries have been deleted successfully."
    except Error as e:
        return f"Error resetting database: {e}"


# Setting up the database
database = r"./Address-Book/address_book.db"
sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

# Create or connect to the database file
conn = create_database_file(database)
if conn:
    create_table(conn, sql_create_tasks_table)
else:
    print("Error: cannot create the database connection.")
```

<hr>

### Generated Output

```
```python
import unittest
import sqlite3
from your_module import *  # Import your module here

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Sets up a test database for each test case."""
        global list_of_names 
        list_of_names = [] # Reset the global list of names before each test
        database = r"./test_address_book.db"  # Use a separate test database
        self.conn = create_database_file(database)
        self.assertTrue(self.conn is not None, "Database connection failed")
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Cleans up the test database after each test case."""
        reset_all_tasks(self.conn)  
        self.conn.close()

    # Positive Cases 
    def test_create_database_success(self):
        self.assertTrue(os.path.exists("./test_address_book.db"))

    def test_add_task_success(self):
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_update_task_success(self):
        add_task(self.conn, "Bob", "9876543210")
        result = update_task(self.conn, "Bob", "1111111111")
        self.assertEqual(result, "Bob updated successfully.")

    def test_delete_task_success(self):
        add_task(self.conn, "Charlie", "2222222222")
        result = delete_task(self.conn, "Charlie")
        self.assertEqual(result, "Charlie deleted successfully.")

    # Edge Cases
    def test_add_task_duplicate_name(self):
        add_task(self.conn, "David", "3333333333")
        result = add_task(self.conn, "David", "4444444444")
        self.assertEqual(result, "Error: David already exists.")

    def test_add_task_empty_name(self):
        result = add_task(self.conn, "", "5555555555")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_number(self):
        result = add_task(self.conn, "Emily", "1234567")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    # Negative Cases (Should raise exceptions)
    def test_create_database_file_already_exists(self):  
        conn = create_database_file(r"./test_address_book.db")  
        with self.assertRaises(sqlite3.Error) as e: # Use an AssertRaises to check for errors
            create_database_file(r"./test_address_book.db") 

    def test_add_task_connection_error(self):
        # Simulate a database connection error
        with self.assertRaises(sqlite3.Error) as e: 
            conn = sqlite3.connect(":memory:")
            conn.close()  
            add_task(conn, "Fake Name", "1234567890") 

if __name__ == "__main__":
    unittest.main()



```


**Explanation:**

- **`setUp()` and `tearDown()`:** These methods are crucial for setting up a clean testing environment.  
    - `setUp()` creates the test database (`test_address_book.db`) before each test case. This ensures that tests are isolated from each other. 
    - `tearDown()` closes the connection and resets the database after each test, preventing data from interfering with subsequent tests.

- **Test Cases:** Each test method covers a specific aspect of the database functions:
    - **Positive Cases:** Verify that the functions work as expected under normal conditions.
    - **Edge Cases:** Test scenarios that push the boundaries of input (e.g., empty names, invalid phone numbers). This helps identify potential bugs or unexpected behavior.
    - **Negative Cases:** Attempt to trigger errors (e.g., duplicate names, database connection issues).

- **Assertions:** The `assertEqual()`, `assertTrue()`, and `assertRaises()` methods are used to verify the outcome of each test case. 

    -  `assertEqual(a, b)`: Checks if two values (`a` and `b`) are equal.
    -  `assertTrue(x)`: Verifies that a condition (`x`) is True.
    -  `assertRaises(ExceptionType, callable, *args, **kwargs)`:  Checks whether calling a function (`callable`) with given arguments (`*args`, `**kwargs`) raises a specific exception type (`ExceptionType`).

- **Test Runner:** The `if __name__ == "__main__":` block ensures that the tests are executed when you run the script.



Let me know if you have any other questions!
```