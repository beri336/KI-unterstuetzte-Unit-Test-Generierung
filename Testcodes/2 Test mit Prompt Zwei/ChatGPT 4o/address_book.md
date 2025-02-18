# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: ChatGPT 4o

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
Here’s a unit test for your provided Python code. It uses the `unittest` framework and includes a variety of test cases, including edge cases and special cases. Make sure to install the `unittest` module (bundled with Python) and run this script in a separate test file.

### Unit Test Code

```python
import unittest
import os
import sqlite3
from your_script_name import (
    create_database_file, create_connection, create_table, add_task, update_task, 
    delete_task, view_task_by_name, view_all_tasks, reset_all_tasks
)

class TestAddressBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the database for testing."""
        cls.test_db = "./test_address_book.db"
        cls.conn = create_database_file(cls.test_db)
        cls.create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                  );"""
        create_table(cls.conn, cls.create_table_sql)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def setUp(self):
        """Reset the database before each test."""
        reset_all_tasks(self.conn)
    
    def test_create_database_file(self):
        """Test creating a new database file."""
        test_file = "./new_test_db.db"
        conn = create_database_file(test_file)
        self.assertTrue(os.path.exists(test_file))
        conn.close()
        os.remove(test_file)
    
    def test_add_task_success(self):
        """Test adding a new task successfully."""
        response = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(response, "Alice added successfully.")
    
    def test_add_task_duplicate_name(self):
        """Test adding a task with a duplicate name."""
        add_task(self.conn, "Alice", "1234567890")
        response = add_task(self.conn, "Alice", "0987654321")
        self.assertEqual(response, "Error: Alice already exists.")
    
    def test_add_task_invalid_phone_number(self):
        """Test adding a task with an invalid phone number."""
        response = add_task(self.conn, "Alice", "12345")
        self.assertEqual(response, "Error: Name cannot be empty, and phone number must be 10 digits.")
    
    def test_update_task_success(self):
        """Test updating an existing task."""
        add_task(self.conn, "Alice", "1234567890")
        response = update_task(self.conn, "Alice", "0987654321")
        self.assertEqual(response, "Alice updated successfully.")
    
    def test_update_task_not_found(self):
        """Test updating a task that does not exist."""
        response = update_task(self.conn, "Bob", "0987654321")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_delete_task_success(self):
        """Test deleting an existing task."""
        add_task(self.conn, "Alice", "1234567890")
        response = delete_task(self.conn, "Alice")
        self.assertEqual(response, "Alice deleted successfully.")
    
    def test_delete_task_not_found(self):
        """Test deleting a task that does not exist."""
        response = delete_task(self.conn, "Bob")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_view_task_by_name_success(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Alice", "1234567890")
        result = view_task_by_name(self.conn, "Alice")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Alice")
    
    def test_view_task_by_name_not_found(self):
        """Test viewing a task that does not exist."""
        response = view_task_by_name(self.conn, "Bob")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_view_all_tasks(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 2)
    
    def test_reset_all_tasks(self):
        """Test resetting all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        response = reset_all_tasks(self.conn)
        self.assertEqual(response, "All entries have been deleted successfully.")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
```

### Key Features of the Test Suite:
1. **Setup and Cleanup**: Ensures that each test runs in isolation by resetting the database in `setUp()` and removing the test database after all tests.
2. **Coverage**: Tests all main functionalities (`add_task`, `update_task`, `delete_task`, `view_task_by_name`, etc.).
3. **Edge Cases**:
   - Invalid phone numbers.
   - Nonexistent tasks for update and delete operations.
   - Duplicate task addition.
   - Reset functionality.
4. **Assertions**: Verifies the correctness of responses and database states.

Make sure to replace `your_script_name` with the actual name of your script file when importing functions. Save this test code in a separate file (e.g., `test_address_book.py`) and run it using `python -m unittest test_address_book.py`.
```