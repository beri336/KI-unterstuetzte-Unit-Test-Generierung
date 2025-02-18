# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: LLama3.2:3b

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
Here's an example of how you can write unit tests for the given Python code using the `unittest` framework.

```python
import unittest
from sqlite3 import Error
from your_module import (
    list_of_names,  # assuming the global list is in a separate module
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
        self.database = r"./Address-Book/address_book.db"
        # Create the table and connection before each test
        self.conn = create_connection(self.database)
        create_table(self.conn, """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );""")
        
    def tearDown(self):
        # Reset the global list of names after each test
        global list_of_names
        list_of_names = []
        self.close_connection()

    def close_connection(self):
        if hasattr('conn', 'close'):
            self.conn.close()

    def test_create_database_file_success(self):
        """Test that create_database_file creates a new SQLite database file."""
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_failure(self):
        """Test that create_database_file fails when creating a non-existent directory."""
        import os
        os.makedirs("/non/existent/dir")
        with self.assertRaises(Error) as e:
            create_database_file("/non/existent/dir")

    def test_create_connection_success(self):
        """Test that create_connection connects to the existing database file."""
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_connection_failure(self):
        """Test that create_connection fails when creating a new directory with no permissions."""
        import os
        os.makedirs("/new/dir")
        with self.assertRaises(Error) as e:
            create_connection("/new/dir")

    def test_add_task_success(self):
        """Test that add_task adds a new task to the database."""
        conn = self.conn
        name = "John Doe"
        number = "1234567890"
        result = add_task(conn, name, number)
        self.assertIn(name, [student[1] for student in view_all_tasks(conn)])

    def test_add_task_duplicate(self):
        """Test that add_task returns an error when trying to add a duplicate task."""
        conn = self.conn
        name = "John Doe"
        number = "1234567890"
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_empty_name(self):
        """Test that add_task returns an error when the task name is empty."""
        conn = self.conn
        name = ""
        number = "1234567890"
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_empty_number(self):
        """Test that add_task returns an error when the task phone number is empty."""
        conn = self.conn
        name = "John Doe"
        number = ""
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_invalid_number(self):
        """Test that add_task returns an error when the task phone number is not 10 digits."""
        conn = self.conn
        name = "John Doe"
        number = "12345678901"  # 11 digits instead of 10
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_update_task_success(self):
        """Test that update_task updates a task's phone number."""
        conn = self.conn
        name = "John Doe"
        original_number = "1234567890"
        new_number = "9876543210"
        result = add_task(conn, name, original_number)
        updated_result = update_task(conn, name, new_number)
        self.assertIn(name, [student[1] for student in view_all_tasks(conn)])
        # Check that the task's phone number has been updated
        updated_row = view_task_by_name(conn, name)[0]
        self.assertEqual(updated_row[2], new_number)

    def test_update_task_failure(self):
        """Test that update_task returns an error when trying to update a non-existent task."""
        conn = self.conn
        name = "John Doe"
        original_number = "1234567890"
        new_number = "9876543210"
        result = add_task(conn, name, original_number)
        with self.assertRaises(Error) as e:
            update_task(conn, name, new_number)

    def test_delete_task_success(self):
        """Test that delete_task deletes a task from the database."""
        conn = self.conn
        name = "John Doe"
        result = add_task(conn, name, "1234567890")
        deleted_result = delete_task(conn, name)
        self.assertNotIn(name, [student[1] for student in view_all_tasks(conn)])

    def test_delete_task_failure(self):
        """Test that delete_task returns an error when trying to delete a non-existent task."""
        conn = self.conn
        result = delete_task(conn, "John Doe")

    def test_view_all_tasks_success(self):
        """Test that view_all_tasks returns all tasks in the database."""
        conn = self.conn
        name1 = "John Doe"
        name2 = "Jane Smith"
        result1 = add_task(conn, name1, "1234567890")
        result2 = add_task(conn, name2, "0987654321")
        self.assertEqual(len(view_all_tasks(conn)), 2)

    def test_view_all_tasks_failure(self):
        """Test that view_all_tasks returns an error when the database connection is closed."""
        conn = None
        with self.assertRaises(Error) as e:
            view_all_tasks(conn)

    def test_reset_all_tasks_success(self):
        """Test that reset_all_tasks resets the global list of names."""
        global list_of_names
        name1 = "John Doe"
        name2 = "Jane Smith"
        result1 = add_task(list_of_names, name1, "1234567890")
        result2 = add_task(list_of_names, name2, "0987654321")
        reset_all_tasks()
        self.assertEqual(len(list_of_names), 0)

if __name__ == '__main__':
    unittest.main()
```

Note: The tests are written for the provided functions and might need to be adjusted based on actual implementation details. Also, please make sure that all necessary modules and imports are included in your Python environment.
```