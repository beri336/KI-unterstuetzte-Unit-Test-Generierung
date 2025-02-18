import os
import sqlite3
from sqlite3 import Error
import unittest

# Test data
test_names = ['John', 'Alice', 'Bob']
test_numbers = [1234567890, 9876543210]

class TestAddressBookDatabase(unittest.TestCase):

    def setUp(self):
        # Create a new test database file
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            status_id integer NOT NULL
                                        );"""
        self.conn = create_database_file(self.database)
        if self.conn:
            # Create the table in the test database
            create_table(self.conn, self.sql_create_tasks_table)

    def tearDown(self):
        # Reset the global list of names
        global list_of_names
        list_of_names = []
        # Delete the test database file
        os.remove(self.database)
        # Close the database connection
        if self.conn:
            self.conn.close()

    def test_create_database_file(self):
        """Test creating a new SQLite database file."""
        # Test case 1: Database file already exists
        db_file = r"./Address-Book/address_book.db"
        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)
        
        # Test case 2: Directory for the database file does not exist
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        db_file_exists = os.path.exists(db_file)
        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)
        # Verify that the directory is created
        self.assertTrue(os.path.exists(db_dir))

    def test_create_connection(self):
        """Test creating a database connection."""
        # Test case 1: Database file exists and connection is successful
        db_file = r"./Address-Book/address_book.db"
        conn = create_connection(db_file)
        self.assertIsNotNone(conn)
        
        # Test case 2: Database file does not exist or connection fails
        db_file_exists = os.path.exists(db_file)
        if not db_file_exists:
            conn = create_connection(db_file)
            self.assertIsNone(conn)

    def test_create_table(self):
        """Test creating a table from the create_table_sql statement."""
        # Test case 1: Table creation is successful
        sql = "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY, name text NOT NULL, status_id integer NOT NULL)"
        conn = self.conn
        create_table(conn, sql)
        cursor = conn.cursor()
        query_result = cursor.execute("SELECT * FROM tasks").fetchone()
        self.assertIsNotNone(query_result)
        
        # Test case 2: Table creation fails due to SQL syntax error
        with self.assertRaises(Error):
            create_table(conn, "Invalid SQL")

    def test_add_task(self):
        """Test adding a new task (contact) to the address book."""
        # Test case 1: Task addition is successful
        conn = self.conn
        name = 'John'
        number = test_numbers[0]
        result = add_task(conn, name, number)
        self.assertIn(name, list_of_names)
        
        # Test case 2: Duplicate task
        with self.assertRaises(ValueError):
            add_task(conn, name, number)

    def test_update_task(self):
        """Test updating the phone number of an existing task."""
        # Test case 1: Task update is successful
        conn = self.conn
        name = 'John'
        number = test_numbers[0]
        result = add_task(conn, name, number)
        updated_number = test_numbers[1]
        result = update_task(conn, name, updated_number)
        self.assertEqual(updated_number, list_of_names[-1])
        
        # Test case 2: Task not found
        with self.assertRaises(ValueError):
            update_task(conn, 'Jane', '1234567890')

    def test_delete_task(self):
        """Test deleting a task by name."""
        # Test case 1: Task deletion is successful
        conn = self.conn
        name = 'John'
        result = add_task(conn, name, test_numbers[0])
        result = delete_task(conn, name)
        self.assertNotIn(name, list_of_names)
        
        # Test case 2: Task not found
        with self.assertRaises(ValueError):
            delete_task(conn, 'Jane')

    def test_view_task_by_name(self):
        """Test querying a task by name."""
        # Test case 1: Task found and returned correctly
        conn = self.conn
        name = 'John'
        result = add_task(conn, name, test_numbers[0])
        rows = view_task_by_name(conn, name)
        self.assertEqual(len(rows), 1)

    def test_view_all_tasks(self):
        """Test getting all rows in the tasks table."""
        # Test case 1: All tasks are returned correctly
        conn = self.conn
        result = add_task(conn, 'Alice', test_numbers[0])
        result = add_task(conn, 'Bob', test_numbers[1])
        rows = view_task_by_name(conn, 'Alice')
        all_tasks = ['Alice', '1234567890']
        self.assertEqual(len(rows), 2)
        for i in range(2):
            self.assertIn(all_tasks[i], [row[0] for row in rows])

if __name__ == '__main__':
    unittest.main()