# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: ChatGPT 4o

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
Below is a unit test suite written for the provided code. It uses Python's built-in `unittest` framework. The test suite includes positive, negative, edge cases, and performance considerations where applicable.

### Test Code

```python
import unittest
import os
import sqlite3
from your_module import create_database_file, create_connection, create_table, add_task, update_task, delete_task, view_task_by_name, view_all_tasks, reset_all_tasks

class TestAddressBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment: Create a temporary database for testing."""
        cls.test_db = "./test_address_book.db"
        cls.create_tasks_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        cls.conn = create_database_file(cls.test_db)
        if cls.conn:
            create_table(cls.conn, cls.create_tasks_table_sql)

    @classmethod
    def tearDownClass(cls):
        """Clean up: Remove the temporary database."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        """Reset the database before each test."""
        reset_all_tasks(self.conn)

    # Positive Test Cases
    def test_add_task_success(self):
        """Test adding a task successfully."""
        result = add_task(self.conn, "John Doe", "1234567890")
        self.assertEqual(result, "John Doe added successfully.")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 1)

    def test_view_task_by_name_success(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Jane Doe", "0987654321")
        task = view_task_by_name(self.conn, "Jane Doe")
        self.assertEqual(task[0][1], "Jane Doe")

    # Edge Cases
    def test_add_task_empty_name(self):
        """Test adding a task with an empty name."""
        result = add_task(self.conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_length(self):
        """Test adding a task with an invalid phone number length."""
        result = add_task(self.conn, "John Doe", "12345")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_not_found(self):
        """Test updating a task that does not exist."""
        result = update_task(self.conn, "Nonexistent", "1111111111")
        self.assertEqual(result, "Error: Nonexistent not found.")

    # Negative Test Cases
    def test_add_duplicate_task(self):
        """Test adding a duplicate task."""
        add_task(self.conn, "John Doe", "1234567890")
        result = add_task(self.conn, "John Doe", "1234567890")
        self.assertEqual(result, "Error: John Doe already exists.")

    def test_delete_task_not_found(self):
        """Test deleting a task that does not exist."""
        result = delete_task(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_view_task_not_found(self):
        """Test viewing a task that does not exist."""
        result = view_task_by_name(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    # Performance Test Cases
    def test_add_large_number_of_tasks(self):
        """Test adding a large number of tasks to measure performance."""
        for i in range(1000):
            name = f"Task{i}"
            number = f"{i:010d}"
            result = add_task(self.conn, name, number)
            self.assertEqual(result, f"{name} added successfully.")

        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 1000)

    def test_reset_all_tasks_performance(self):
        """Test performance of resetting all tasks with many entries."""
        for i in range(1000):
            name = f"Task{i}"
            number = f"{i:010d}"
            add_task(self.conn, name, number)

        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 0)

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases

1. **Positive Cases**:
   - `test_add_task_success`: Verifies normal operation of adding a task.
   - `test_view_task_by_name_success`: Checks if a task can be viewed successfully after being added.

2. **Edge Cases**:
   - `test_add_task_empty_name`: Handles empty input for the `name` parameter.
   - `test_add_task_invalid_phone_length`: Tests incorrect phone number length.

3. **Negative Cases**:
   - `test_add_duplicate_task`: Tests behavior when adding a task with a duplicate name.
   - `test_delete_task_not_found`: Handles deletion of a non-existent task.
   - `test_view_task_not_found`: Handles retrieval of a non-existent task.

4. **Performance Cases**:
   - `test_add_large_number_of_tasks`: Measures the behavior and correctness when adding many entries.
   - `test_reset_all_tasks_performance`: Evaluates performance when resetting a large database.

### Notes

- Replace `your_module` with the actual name of the Python file containing your implementation.
- Ensure the tests are run in an isolated environment to avoid conflicts with other databases or data.
- Performance tests might be adjusted based on system capabilities and expected load.
```