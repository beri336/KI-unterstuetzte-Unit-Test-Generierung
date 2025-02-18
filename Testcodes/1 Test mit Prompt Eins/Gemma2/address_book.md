# Unit Test Documentation
## Original File: ../Address-Book/address_book.py

### Model: Gemma2:9b

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
```python
import unittest
from sqlite3 import Error  
from your_module import *  # Import your module here 

class TestAddressBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database = r"./test_address_book.db"  # Use a temporary database for testing
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );"""

        try:
            conn = create_database_file(cls.database) 
            if conn:
                create_table(conn, sql_create_tasks_table)
                conn.close()  # Close the connection after creating the table
            else:
                print("Error: cannot create the database connection.")
        except Error as e:
            print(f"Error creating test database: {e}")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.database) # Remove the temporary database after testing

    def test_create_database_file(self):
        conn = create_database_file(self.database)  # Test with a different filename
        self.assertIsNotNone(conn, "Database connection should not be None")
        conn.close() 

    def test_add_task(self):
        conn = create_connection(self.database) 
        result = add_task(conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.", "Task should be added successfully")
        conn.close()

    def test_add_duplicate_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "Bob", "9876543210")  
        result = add_task(conn, "Bob", "1234567890")
        self.assertEqual(result, "Error: Bob already exists.", "Duplicate task should not be added") 
        conn.close()

    def test_update_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "Charlie", "1234567890")  
        result = update_task(conn, "Charlie", "9876543210")
        self.assertEqual(result, "Charlie updated successfully.", "Task should be updated") 
        conn.close()

    def test_delete_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "David", "1234567890")  
        result = delete_task(conn, "David")
        self.assertEqual(result, "David deleted successfully.", "Task should be deleted") 
        conn.close()

    def test_view_all_tasks(self):
        conn = create_connection(self.database) 
        add_task(conn, "Emily", "1234567890")  
        result = view_all_tasks(conn)
        self.assertIsNotNone(result) 
        conn.close()

    def test_view_task_by_name(self):
        conn = create_connection(self.database) 
        add_task(conn, "Frank", "1234567890")  
        result = view_task_by_name(conn, "Frank")
        self.assertIsNotNone(result) 
        conn.close()

    # Add more tests as needed



if __name__ == '__main__':
    unittest.main()
```


**Explanation:**

1. **Import Necessary Modules:** Import `unittest` for testing and your module containing the address book functions.
2. **Class Setup:**
   - Create a test class inheriting from `unittest.TestCase`.
   - Use `@classmethod setUpClass` to set up a temporary database file (`test_address_book.db`) for each test run. 
   -  Create the `tasks` table within this temporary database.
3. **Test Functions:** Write individual test functions (starting with `test_...`) to test specific functionalities:
   - `test_create_database_file`: Test if `create_database_file` creates a valid connection.
   - `test_add_task`, `test_add_duplicate_task`: Test adding tasks, including handling duplicates.
   - `test_update_task`, `test_delete_task`: Test updating and deleting existing tasks.
   - `test_view_all_tasks`, `test_view_task_by_name`: Test retrieving tasks.

4. **Assertions:** Use `assertEqual`, `assertIsNotNone`, or other assertions from the `unittest` module to verify expected results.

5. **Teardown:** Use `@classmethod tearDownClass` to remove the temporary database file after all tests are complete.



**Remember:**
- Replace `"your_module"` with the actual name of your Python module containing the address book functions. 
```