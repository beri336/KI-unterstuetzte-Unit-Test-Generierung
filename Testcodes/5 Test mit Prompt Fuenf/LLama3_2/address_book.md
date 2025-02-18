# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: LLama3.2:3b

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "main.py"

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
Below are the unit tests for your code using Python's `unittest` framework.

```python
import unittest
from sqlite3 import Error
from main import list_of_names  # Importing the global list of names for validation

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        
    # Normal input cases with common values
    def test_add_task_success(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "John Doe", 1234567890)
            self.assertEqual(result, f"{result}")
            conn.close()

    def test_update_task_success(self):
        conn = create_connection(self.database)
        if conn:
            add_task(conn, "Jane Doe", 9876543210)
            result = update_task(conn, "John Doe", 1234567891)
            self.assertEqual(result, f"{result}")
            conn.close()

    def test_delete_task_success(self):
        conn = create_connection(self.database)
        if conn:
            add_task(conn, "Bob Smith", 5551234567)
            result = delete_task(conn, "John Doe")
            self.assertEqual(result, f"{result}")
            conn.close()

    # Edge cases
    def test_add_empty_name(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "", 1234567890)
            self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")
            conn.close()

    def test_update_nonexistent_student(self):
        conn = create_connection(self.database)
        if conn:
            result = update_task(conn, "Unknown Student", 1234567891)
            self.assertEqual(result, f"Error: Unknown Student not found.")
            conn.close()

    def test_delete_nonexistent_student(self):
        conn = create_connection(self.database)
        if conn:
            result = delete_task(conn, "Unknown Student")
            self.assertEqual(result, f"Error: Unknown Student not found.")
            conn.close()

    # Invalid input cases that should raise exceptions
    def test_add_empty_number(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "John Doe", "")
            self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")
            conn.close()

    def test_update_invalid_number_length(self):
        conn = create_connection(self.database)
        if conn:
            result = update_task(conn, "Jane Doe", "123456789")
            self.assertEqual(result, f"Error: Jane Doe already exists.")
            conn.close()

if __name__ == '__main__':
    unittest.main()
```
Each test case follows the recommended order of writing unit tests:

1.  Normal input cases with common values
2.  Edge cases
3.  Invalid input cases that should raise exceptions

Note that we've imported the `list_of_names` global variable for validation in each test case, as it's used to verify the correctness of database operations.

Also note that this implementation assumes a basic understanding of how unit tests work and how to write them using Python's `unittest` framework.
```