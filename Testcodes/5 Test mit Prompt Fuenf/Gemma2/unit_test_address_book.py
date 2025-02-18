import unittest
import main  # Import your code

class TestAddressBookFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a new database file for each test."""
        cls.database = r"./test_address_book.db"
        main.create_database_file(cls.database) 
        conn = main.create_connection(cls.database)
        if conn:
            conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, status_id INTEGER)")  # Create table

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests."""
        os.remove(cls.database) 

    def test_create_table(self):
        """Test that the table is created successfully."""
        conn = main.create_connection(self.database)
        main.create_table(conn, "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, status_id INTEGER)") 
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_add_task_normal_case(self):
        """Test adding a new task with valid input."""
        conn = main.create_connection(self.database)
        result = main.add_task(conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_add_task_duplicate_name(self):
        """Test adding a duplicate task name."""
        conn = main.create_connection(self.database)
        main.add_task(conn, "Bob", "9876543210")
        result = main.add_task(conn, "Bob", "1111111111")
        self.assertEqual(result, "Error: Bob already exists.")

    def test_add_task_invalid_name(self):
        """Test adding a task with an empty name."""
        conn = main.create_connection(self.database)
        result = main.add_task(conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_number(self):
        """Test adding a task with an invalid phone number."""
        conn = main.create_connection(self.database)
        result = main.add_task(conn, "Charlie", "12345678")  # Too short
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_valid(self):
        """Test updating an existing task."""
        conn = main.create_connection(self.database)
        main.add_task(conn, "David", "2345678901")
        result = main.update_task(conn, "David", "3456789012")
        self.assertEqual(result, "David updated successfully.")

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task."""
        conn = main.create_connection(self.database)
        result = main.update_task(conn, "Eve", "4567890123")
        self.assertEqual(result, "Error: Task 'Eve' not found.")

    def test_view_all_tasks_empty(self):
        """Test viewing all tasks when the table is empty."""
        conn = main.create_connection(self.database)
        results = main.view_all_tasks(conn)
        self.assertEqual(len(results), 0)

    def test_view_all_tasks_populated(self):
        """Test viewing all tasks after adding some."""
        conn = main.create_connection(self.database)
        main.add_task(conn, "Frank", "5678901234")
        main.add_task(conn, "Grace", "6789012345")
        results = main.view_all_tasks(conn)
        self.assertGreaterEqual(len(results), 2)

    def test_reset_all_tasks(self):
        """Test resetting all tasks."""
        conn = main.create_connection(self.database)
        main.add_task(conn, "Henry", "7890123456")
        result = main.reset_all_tasks(conn)
        self.assertEqual(result, "All entries have been deleted successfully.")



if __name__ == '__main__':
    unittest.main()   