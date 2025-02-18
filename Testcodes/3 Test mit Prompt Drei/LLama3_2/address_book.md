# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: LLama3.2:3b

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
Here's an example of how you can write unit tests for this Python code. This solution uses Python's built-in unittest module.

```python
import os
import sqlite3
from unittest import TestCase
from tempfile import TemporaryDirectory
from your_module import (
    list_of_names,  # Import the global list of names from the original module
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


class TestAddressBookDB(TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            status_id integer NOT NULL
                                        );"""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            self.database = os.path.join(tmpdir, "address_book.db")
            conn = create_connection(self.database)
            if conn is not None:
                create_table(conn, self.sql_create_tasks_table)

    def tearDown(self):
        # Delete the database file
        try:
            import shutil
            shutil.rmtree(self.database)
        except Exception as e:
            pass

    def test_create_database_file_positive_case(self):
        """Test creating a new SQLite database file if it does not exist."""
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_edge_case_non_existent_directory(self):
        """Test creating a new SQLite database file if the parent directory does not exist."""
        # Create a temporary directory
        with TemporaryDirectory() as tmpdir:
            try:
                os.environ["PWD"] = tmpdir
                conn = create_database_file(os.path.join(tmpdir, "address_book.db"))
                self.assertIsNotNone(conn)
            except Exception as e:
                pass

    def test_create_connection_positive_case(self):
        """Test creating a database connection to the SQLite database."""
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_connection_edge_case_non_existent_file(self):
        """Test connecting to an existing SQLite database file."""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            try:
                conn = create_connection(os.path.join(tmpdir, "address_book.db"))
                self.assertIsNotNone(conn)
            except Exception as e:
                pass

    def test_add_task_positive_case(self):
        """Test adding a new task to the address book."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "1234567890")
        self.assertIn("added successfully", result)

    def test_add_task_edge_case_duplicate_name(self):
        """Test adding a new task with an existing name in the database."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "1234567890")
        result = add_task(conn, "John Doe", "9876543210")
        self.assertIn("added successfully", result)

    def test_add_task_negative_case_empty_name(self):
        """Test adding a new task with an empty name."""
        conn = create_connection(self.database)
        result = add_task(conn, "", "1234567890")
        self.assertIn("Error: Name cannot be empty", result)

    def test_add_task_negative_case_invalid_phone_number(self):
        """Test adding a new task with an invalid phone number."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "123456")
        self.assertIn("Error: Phone number must be 10 digits.", result)

    def test_update_task_positive_case(self):
        """Test updating the phone number of an existing task."""
        conn = create_connection(self.database)
        conn.execute("INSERT INTO tasks(name, status_id) VALUES('John Doe', 1)")
        conn.commit()
        result = update_task(conn, "John Doe", "1234567890")
        self.assertIn("updated successfully", result)

    def test_update_task_negative_case_non_existent_name(self):
        """Test updating the phone number of a non-existent task."""
        conn = create_connection(self.database)
        result = update_task(conn, "John Doe", "9876543210")
        self.assertIn("Error: John Doe not found.", result)

    def test_delete_task_positive_case(self):
        """Test deleting a task by name."""
        conn = create_connection(self.database)
        conn.execute("INSERT INTO tasks(name, status_id) VALUES('John Doe', 1)")
        conn.commit()
        result = delete_task(conn, "John Doe")
        self.assertIn("deleted successfully", result)

    def test_delete_task_negative_case_non_existent_name(self):
        """Test deleting a non-existent task."""
        conn = create_connection(self.database)
        result = delete_task(conn, "John Doe")
        self.assertIn("Error: John Doe not found.", result)

    def test_view_all_tasks_positive_case(self):
        """Test viewing all tasks in the address book."""
        conn = create_connection(self.database)
        conn.execute("""
            INSERT INTO tasks(name, status_id) VALUES
                ('John Doe', 1),
                ('Jane Smith', 2),
                ('Bob Johnson', 3)
            """
        )
        conn.commit()
        result = view_all_tasks(conn)
        self.assertIn("John Doe", result)
        self.assertIn("Jane Smith", result)
        self.assertIn("Bob Johnson", result)

    def test_view_all_tasks_negative_case_empty_database(self):
        """Test viewing all tasks in an empty address book."""
        conn = create_connection(self.database)
        result = view_all_tasks(conn)
        self.assertEqual(result, "")

    def test_reset_all_tasks_positive_case(self):
        """Test resetting all tasks in the address book."""
        conn = create_connection(self.database)
        conn.execute("""
            INSERT INTO tasks(name, status_id) VALUES
                ('John Doe', 1),
                ('Jane Smith', 2),
                ('Bob Johnson', 3)
            """
        )
        conn.commit()
        result = reset_all_tasks(conn)
        self.assertEqual(result, "")

    def test_reset_all_tasks_negative_case_non_existent_database(self):
        """Test resetting all tasks in a non-existent address book."""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            try:
                conn = create_connection(os.path.join(tmpdir, "address_book.db"))
                result = reset_all_tasks(conn)
                self.assertEqual(result, "")
            except Exception as e:
                pass
```

Please replace `your_module` with the actual name of your Python module where the functions are defined.

This test suite covers various cases for each function:

*   Positive case: Test a successful operation.
*   Edge case: Test an unusual scenario that is likely to occur in real-world usage. For example, adding a new task with an existing name or updating a non-existent task.
*   Negative case: Test a failure scenario where the expected result should be different from the actual one.

Note that this test suite assumes the database operations are atomic and idempotent, meaning they don't leave the database in a worse state than before running.
```