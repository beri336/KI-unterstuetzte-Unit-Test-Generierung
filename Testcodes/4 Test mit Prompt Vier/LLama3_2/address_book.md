# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: LLama3.2:3b

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
To write unit tests for the provided Python code, we'll use the `unittest` framework. We'll define separate test functions to cover various scenarios.

Firstly, let's import the necessary modules and classes from the `unittest` package:

```python
import unittest
from sqlite3 import Error
```

Now, let's start with testing individual functions separately:

### 1. `create_database_file(db_file)` function

We'll test this function by creating a database file that doesn't exist, checking if it exists after creation, and verifying the database connection.

```python
class TestDatabaseFunctions(unittest.TestCase):

    def test_create_database_file_exists(self):
        # Create a temporary file that exists
        db_file = "test.db"
        with open(db_file, "w") as f:
            pass

        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)  # Ensure connection is not None
        with self.assertRaises(Error):  # Check if creation fails for an existing file
            create_database_file(db_file)

    def test_create_database_file_does_not_exist(self):
        # Create a temporary file that doesn't exist
        db_file = "test.db"

        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)  # Ensure connection is not None

    def tearDown(self):
        import os
        # Remove the database file created during testing
        if os.path.exists("test.db"):
            os.remove("test.db")
```

### 2. `create_connection(db_file)` function

We'll test this function by creating a new SQLite database file and verifying that it can be successfully connected to.

```python
def test_create_connection_valid_input(self):
    # Create a temporary file
    db_file = "test.db"

    conn = create_connection(db_file)
    self.assertIsNotNone(conn)  # Ensure connection is not None

def test_create_connection_invalid_input(self):
    # Create a database file with an invalid path (should fail)
    db_file = "/invalid/path/test.db"

    conn = create_connection(db_file)
    self.assertIsNone(conn)  # Ensure connection is None
```

### 3. `create_table(conn, create_table_sql)` function

We'll test this function by creating a table that doesn't exist and verifying that it can be successfully created.

```python
def test_create_table_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""
    create_table(conn, sql_create_tasks_table)
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure table exists

def test_create_table_invalid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = "CREATE TABLE IF NOT EXISTS invalid_table( id integer PRIMARY KEY, name text NOT NULL )"
    with self.assertRaises(Error):  # Check if creation fails for an invalid table
        create_table(conn, sql_create_tasks_table)
```

### 4. `add_task(conn, name, number)` function

We'll test this function by adding a new task and verifying that it can be successfully added.

```python
def test_add_task_valid_input(self):
    # Create a temporary file
    db_file = "test.db"

    conn = create_connection(db_file)
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertEqual(len(list_of_names), 1)  # Ensure the task is added successfully

def test_add_task_empty_name(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    with self.assertRaises(ValueError):  # Check if the task is not added successfully due to empty name
        add_task(conn, "", "1234567890")

def test_add_task_invalid_phone_number(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    with self.assertRaises(ValueError):  # Check if the task is not added successfully due to invalid phone number
        add_task(conn, "Test Name", "123456")  # Invalid phone number
```

### 5. `create_table(conn, create_table_sql)` function

We'll test this function by creating a table that doesn't exist and verifying that it can be successfully created.

```python
def test_create_table_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    create_table(conn, sql_create_tasks_table)
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure table exists

def test_create_table_invalid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = "CREATE TABLE IF NOT EXISTS invalid_table( id integer PRIMARY KEY, name text NOT NULL )"
    with self.assertRaises(Error):  # Check if creation fails for an invalid table
        create_table(conn, sql_create_tasks_table)
```

### 6. `delete_task` function

We'll test this function by deleting a task and verifying that it can be successfully deleted.

```python
def test_delete_task_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure the task exists

    delete_task(conn)
    self.assertFalse(conn.execute("SELECT * FROM tasks").fetchone())  # Ensure the task is deleted successfully
```

### 7. `update_task` function

We'll test this function by updating a task and verifying that it can be successfully updated.

```python
def test_update_task_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure the task exists

    update_task(conn, 1, "Updated Test Name", "1234567890")
    self.assertEqual(conn.execute("SELECT name FROM tasks WHERE id=1").fetchone()[0], "Updated Test Name")  # Ensure the task is updated successfully
```

### Running tests

To run these tests, save them in a file (e.g., `test_database_functions.py`) and execute it using the Python interpreter:

```bash
python test_database_functions.py
```

This will display the test results, indicating whether each test passed or failed.

Remember to install the `unittest` package if you haven't already done so:

```bash
pip install unittest
```
```