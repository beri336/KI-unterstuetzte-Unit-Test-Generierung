# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

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
from main import *

class TestAddressBook(unittest.TestCase):

    def test_add_task_valid_input(self):
        conn = create_connection(database)
        result = add_task(conn, "John Doe", 1234567890)
        self.assertEqual(result, "John Doe added successfully.")

    def test_add_task_invalid_name(self):
        conn = create_connection(database)
        result = add_task(conn, "", 1234567890)
        self.assertEqual(result, "Error: Name cannot be empty.")

    def test_add_task_invalid_number(self):
        conn = create_connection(database)
        result = add_task(conn, "John Doe", "invalid_number")
        self.assertEqual(result, "Error: Phone number must be 10 digits.")

    def test_add_task_duplicate_name(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = add_task(conn, "John Doe", 1234567890)
        self.assertEqual(result, f"Error: John Doe already exists.")

    def test_update_task_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = update_task(conn, "John Doe", 9876543210)
        self.assertEqual(result, "John Doe updated successfully.")

    def test_update_task_invalid_name(self):
        conn = create_connection(database)
        result = update_task(conn, "Nonexistent Name", 9876543210)
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_delete_task_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = delete_task(conn, "John Doe")
        self.assertEqual(result, "John Doe deleted successfully.")

    def test_delete_task_invalid_name(self):
        conn = create_connection(database)
        result = delete_task(conn, "Nonexistent Name")
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_view_task_by_name_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = view_task_by_name(conn, "John Doe")
        self.assertEqual(result[0][1], "John Doe")

    def test_view_task_by_name_invalid_name(self):
        conn = create_connection(database)
        result = view_task_by_name(conn, "Nonexistent Name")
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_view_all_tasks(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        add_task(conn, "Jane Doe", 9876543210)
        result = view_all_tasks(conn)
        self.assertEqual(len(result), 2)

    def test_reset_all_tasks(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = reset_all_tasks(conn)
        self.assertEqual(result, "All entries have been deleted successfully.")

if __name__ == '__main__':
    unittest.main()
```
```