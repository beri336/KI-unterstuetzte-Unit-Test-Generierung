# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "address_book.py"


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
Here's a set of `unittest` cases for the given Python code. These test cases are organized to first validate normal input, then edge cases, and finally invalid input, all with explanatory comments.

### Test Suite

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
    reset_all_tasks,
)

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database for testing."""
        self.db_file = "./test_address_book.db"
        self.conn = create_database_file(self.db_file)
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Clean up by removing the temporary database file."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    # Test normal cases
    def test_add_task_normal(self):
        """Test adding a valid task."""
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_view_task_by_name_normal(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Bob", "0987654321")
        result = view_task_by_name(self.conn, "Bob")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Bob")
        self.assertEqual(result[0][2], 987654321)

    def test_update_task_normal(self):
        """Test updating an existing task's phone number."""
        add_task(self.conn, "Charlie", "1234567890")
        result = update_task(self.conn, "Charlie", "0987654321")
        self.assertEqual(result, "Charlie updated successfully.")
        updated_task = view_task_by_name(self.conn, "Charlie")
        self.assertEqual(updated_task[0][2], 987654321)

    def test_delete_task_normal(self):
        """Test deleting a task by name."""
        add_task(self.conn, "Daisy", "1234567890")
        result = delete_task(self.conn, "Daisy")
        self.assertEqual(result, "Daisy deleted successfully.")
        result = view_task_by_name(self.conn, "Daisy")
        self.assertEqual(result, "Error: Daisy not found.")

    def test_view_all_tasks_normal(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Eve", "1234567890")
        add_task(self.conn, "Frank", "0987654321")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 2)

    # Test edge cases
    def test_add_task_empty_name(self):
        """Test adding a task with an empty name."""
        result = add_task(self.conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_length(self):
        """Test adding a task with a phone number of invalid length."""
        result = add_task(self.conn, "George", "12345")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_nonexistent(self):
        """Test updating a task that does not exist."""
        result = update_task(self.conn, "Nonexistent", "0987654321")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_delete_task_nonexistent(self):
        """Test deleting a task that does not exist."""
        result = delete_task(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_reset_all_tasks_empty(self):
        """Test resetting all tasks when the table is already empty."""
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        self.assertEqual(view_all_tasks(self.conn), [])

    # Test invalid input cases
    def test_add_task_invalid_type(self):
        """Test adding a task with invalid data types."""
        with self.assertRaises(TypeError):
            add_task(self.conn, 123, 456)

    def test_update_task_invalid_type(self):
        """Test updating a task with invalid data types."""
        with self.assertRaises(TypeError):
            update_task(self.conn, 123, 456)

    def test_delete_task_invalid_type(self):
        """Test deleting a task with invalid data types."""
        with self.assertRaises(TypeError):
            delete_task(self.conn, 123)

if __name__ == "__main__":
    unittest.main()
```

### Explanation of the Test Suite
1. **Setup and Teardown**:
   - A temporary database file (`test_address_book.db`) is created and set up before each test.
   - The database file is cleaned up after each test to ensure isolation between tests.

2. **Normal Input Cases**:
   - Validate standard operations such as adding, updating, deleting, and viewing tasks.
   - Check expected behavior for typical valid inputs.

3. **Edge Cases**:
   - Test inputs that are technically valid but unusual (e.g., empty names or invalid phone number lengths).
   - Verify the system handles these cases gracefully.

4. **Invalid Input Cases**:
   - Test inputs that are completely invalid, such as wrong data types, and ensure the appropriate exceptions are raised.

This test suite ensures the robustness of the `address_book.py` module under a variety of scenarios.
```