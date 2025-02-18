# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: Gemma2:9b

<hr>

### Prompt

```
Write me a Unit Test for the following Python Code, write comments and add special cases and edge cases:

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
from unittest.mock import patch
from your_module import (create_database_file, 
                        create_connection, 
                        create_table, 
                        add_task, 
                        update_task, 
                        delete_task, 
                        view_task_by_name, 
                        view_all_tasks, 
                        reset_all_tasks) # Import your functions


class TestAddressBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary database file for testing
        cls.database = r"./test_address_book.db"
        cls.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    @classmethod
    def tearDownClass(cls):
        # Delete the temporary database file after testing
        os.remove(cls.database) 

    def test_create_database_file(self):
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_exists(self):
        # Test when the database file already exists
        conn = create_database_file(self.database)  
        with self.assertRaises(sqlite3.Error): 
            create_database_file(self.database) 

    def test_create_connection(self):
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_table(self):
        # Connect to the database
        conn = sqlite3.connect(self.database)
        create_table(conn, self.sql_create_tasks_table)
        # Check if the table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_add_task(self):
        conn = create_connection(self.database)
        # Add a new task
        result = add_task(conn, "John Doe", "1234567890")
        self.assertEqual(result, "John Doe added successfully.")
        # Check if the task exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE name='John Doe'")
        rows = cursor.fetchall()
        self.assertIsNotNone(rows)

    def test_add_task_duplicate(self):
        conn = create_connection(self.database)
        # Add a duplicate task
        result = add_task(conn, "John Doe", "1234567890")
        self.assertEqual(result, "Error: John Doe already exists.")

    def test_add_task_invalid_name(self):
        conn = create_connection(self.database)
        # Add a task with an empty name
        result = add_task(conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_number(self):
        conn = create_connection(self.database)
        # Add a task with an invalid phone number length
        result = add_task(conn, "Jane Doe", "123456789")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task(self):
        conn = create_connection(self.database)
        # Add a task initially
        add_task(conn, "Alice", "9876543210")

        # Update the task
        result = update_task(conn, "Alice", "5551234567")
        self.assertEqual(result, "Task updated successfully.")

    def test_delete_task(self):
        conn = create_connection(self.database)
        # Add a task initially
        add_task(conn, "Bob", "0987654321")

        # Delete the task
        result = delete_task(conn, "Bob")
        self.assertEqual(result, "Task deleted successfully.")


    def test_view_task_by_name(self):
        conn = create_connection(self.database)
        add_task(conn, "Charlie", "1112223333")

        # View the task by name
        result = view_task_by_name(conn, "Charlie")
        self.assertIsNotNone(result)

    def test_view_all_tasks(self):
        conn = create_connection(self.database)
        add_task(conn, "David", "4445556666")
        add_task(conn, "Emily", "7778889999")

        # View all tasks
        result = view_all_tasks(conn)
        self.assertIsNotNone(result)

    def test_reset_all_entries(self):
        conn = create_connection(self.database)
        add_task(conn, "Frank", "2223334444")

        # Reset all entries
        result = reset_all_tasks(conn)
        self.assertEqual(result, "All entries have been deleted successfully.")



if __name__ == '__main__':
    unittest.main()
``` 

**Key Points and Explanations:**


* **Setup and Teardown:**  The `setUpClass` and `tearDownClass` methods are used to create a temporary database file for testing (`test_address_book.db`) before each test suite and delete it afterward. This ensures that tests don't interfere with each other.

* **Testing Database Interaction:** Most tests directly connect to the database using `sqlite3`. You'll need to make sure the `sqlite3` module is installed.
* **Test Cases:** Each test function (`test_create_database_file`, `test_add_task`, etc.) focuses on a specific aspect of your address book functionality.
* **Assertions:** Assertions like `self.assertEqual`, `self.assertIsNotNone`, and `with self.assertRaises` are used to verify that the code behaves as expected.

**Additional Considerations:**



* **Mocking:** For complex interactions with external systems or dependencies, consider using mocking libraries like `unittest.mock` to isolate your tests.
* **Code Coverage:**  Use a code coverage tool (like `coverage`) to measure how much of your code is exercised by the tests. Aim for high code coverage to ensure thorough testing.
* **Test Organization:** Group related test cases into logical classes and use meaningful names to improve readability and maintainability.



Let me know if you have any more questions!
```