# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following given Python Code:

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
Here's a `unittest`-based suite to test the given Python code. The tests focus on validating the database interactions and key operations, such as adding, updating, deleting, and viewing tasks.

```python
import unittest
import sqlite3
import os
from your_module import create_database_file, create_connection, create_table, add_task, update_task, delete_task, view_task_by_name, view_all_tasks, reset_all_tasks

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database for testing."""
        self.test_db = "./test_address_book.db"
        self.conn = create_database_file(self.test_db)
        self.assertIsNotNone(self.conn, "Database connection should not be None.")
        
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );"""
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Clean up the test database."""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_task(self):
        """Test adding a task to the database."""
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")
        
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Error: Alice already exists.")

    def test_view_task_by_name(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Bob", "0987654321")
        result = view_task_by_name(self.conn, "Bob")
        self.assertTrue(len(result) > 0, "Task should exist.")
        self.assertEqual(result[0][1], "Bob", "Task name should match.")

        result = view_task_by_name(self.conn, "Charlie")
        self.assertEqual(result, "Error: Charlie not found.")

    def test_view_all_tasks(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 2, "There should be two tasks in the database.")

    def test_update_task(self):
        """Test updating a task."""
        add_task(self.conn, "Alice", "1234567890")
        result = update_task(self.conn, "Alice", "0987654321")
        self.assertEqual(result, "Alice updated successfully.")

        result = update_task(self.conn, "Charlie", "0987654321")
        self.assertEqual(result, "Error: Charlie not found.")

    def test_delete_task(self):
        """Test deleting a task."""
        add_task(self.conn, "Alice", "1234567890")
        result = delete_task(self.conn, "Alice")
        self.assertEqual(result, "Alice deleted successfully.")

        result = delete_task(self.conn, "Alice")
        self.assertEqual(result, "Error: Alice not found.")

    def test_reset_all_tasks(self):
        """Test resetting all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 0, "Database should be empty after reset.")

if __name__ == '__main__':
    unittest.main()
```

### Key Points:
1. **`setUp` Method**: Initializes a temporary SQLite database for testing.
2. **`tearDown` Method**: Cleans up the database after tests run.
3. **Individual Test Cases**: Each function in the code is tested for expected behavior.
4. **Assertions**: Verifies the correctness of each operation.

### Usage:
- Replace `your_module` with the name of the file where the provided code resides.
- Run the test suite with `python -m unittest <test_file_name>.py`.

This ensures the code behaves as expected across a variety of scenarios.
```