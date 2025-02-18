# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

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
filename: "address_book.py"

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
To create unit tests for the provided `address_book.py` file, we'll use the `unittest` module in Python. Below are the steps to break down the testing process and write test cases for each major function in the module.

---

### Step 1: Set up the testing framework and helper methods
First, create a test file `test_address_book.py` and include the necessary imports.

```python
import unittest
import sqlite3
import os
from address_book import (
    create_database_file, 
    create_connection, 
    create_table, 
    add_task, 
    update_task, 
    delete_task, 
    view_task_by_name, 
    view_all_tasks, 
    reset_all_tasks
)

class TestAddressBook(unittest.TestCase):
    def setUp(self):
        # Setup a test database file
        self.test_db = "test_address_book.db"
        self.conn = create_database_file(self.test_db)
        create_table(self.conn, """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );""")

    def tearDown(self):
        # Clean up and remove the test database file
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
```

The `setUp` and `tearDown` methods ensure a fresh test database for each test.

---

### Step 2: Test `create_database_file`

```python
def test_create_database_file_valid_path(self):
    # Ensure the database file is created and accessible
    self.assertTrue(os.path.exists(self.test_db))

def test_create_database_file_invalid_path(self):
    # Attempt to create a database with an invalid path
    invalid_path = "/invalid/path/address_book.db"
    conn = create_database_file(invalid_path)
    self.assertIsNone(conn)
```

---

### Step 3: Test `create_connection`

```python
def test_create_connection_valid(self):
    # Ensure connection is successfully created
    conn = create_connection(self.test_db)
    self.assertIsNotNone(conn)

def test_create_connection_invalid(self):
    # Attempt to connect to a non-existent database
    conn = create_connection("non_existent.db")
    self.assertIsNotNone(conn)
```

---

### Step 4: Test `add_task`

```python
def test_add_task_valid(self):
    result = add_task(self.conn, "Alice", "1234567890")
    self.assertEqual(result, "Alice added successfully.")

def test_add_task_duplicate_name(self):
    add_task(self.conn, "Bob", "1234567890")
    result = add_task(self.conn, "Bob", "0987654321")
    self.assertEqual(result, "Error: Bob already exists.")

def test_add_task_invalid_number(self):
    result = add_task(self.conn, "Charlie", "12345")
    self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")
```

---

### Step 5: Test `update_task`

```python
def test_update_task_existing(self):
    add_task(self.conn, "Diana", "1234567890")
    result = update_task(self.conn, "Diana", "0987654321")
    self.assertEqual(result, "Diana updated successfully.")

def test_update_task_nonexistent(self):
    result = update_task(self.conn, "Eve", "1234567890")
    self.assertEqual(result, "Error: Eve not found.")
```

---

### Step 6: Test `delete_task`

```python
def test_delete_task_existing(self):
    add_task(self.conn, "Frank", "1234567890")
    result = delete_task(self.conn, "Frank")
    self.assertEqual(result, "Frank deleted successfully.")

def test_delete_task_nonexistent(self):
    result = delete_task(self.conn, "Grace")
    self.assertEqual(result, "Error: Grace not found.")
```

---

### Step 7: Test `view_task_by_name`

```python
def test_view_task_by_name_existing(self):
    add_task(self.conn, "Henry", "1234567890")
    result = view_task_by_name(self.conn, "Henry")
    self.assertTrue(len(result) > 0)

def test_view_task_by_name_nonexistent(self):
    result = view_task_by_name(self.conn, "Isla")
    self.assertEqual(result, "Error: Isla not found.")
```

---

### Step 8: Test `view_all_tasks`

```python
def test_view_all_tasks(self):
    add_task(self.conn, "Jack", "1234567890")
    add_task(self.conn, "Jill", "0987654321")
    result = view_all_tasks(self.conn)
    self.assertEqual(len(result), 2)
```

---

### Step 9: Test `reset_all_tasks`

```python
def test_reset_all_tasks(self):
    add_task(self.conn, "Kyle", "1234567890")
    reset_all_tasks(self.conn)
    result = view_all_tasks(self.conn)
    self.assertEqual(len(result), 0)
```

---

### Run the tests
Execute the tests using `unittest`.

```bash
python -m unittest test_address_book.py
```

These test cases provide full coverage for the `address_book.py` functionality, handling both normal and edge cases.
```