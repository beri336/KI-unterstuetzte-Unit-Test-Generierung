import unittest
from main import *  # Import all functions from your "main.py" file

class TestAddressBookFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a database connection for testing."""
        cls.database = r"./test_address_book.db" 
        cls.conn = create_database_file(cls.database)  
        if cls.conn:
            create_table(cls.conn, sql_create_tasks_table)

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after testing."""
        reset_all_tasks(cls.conn) 
        cls.conn.close()  

    # Test cases for create_database_file function

    def test_create_database_file_new_db(self):
        """Test creating a new database file successfully."""
        result = create_database_file("./test_address_book_new.db")
        self.assertIsNotNone(result)  # Check if connection object is returned

    def test_create_database_file_existing_db(self):
        """Test connecting to an existing database file."""
        conn = create_database_file("./test_address_book.db")
        self.assertIsNotNone(conn) 

    # Test cases for create_connection function

    def test_create_connection_success(self):
        """Test creating a successful connection to the database."""
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)  
        conn.close() 

    # Test cases for add_task function

    def test_add_task_valid_input(self):
        """Test adding a new task with valid input."""
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_add_task_duplicate_name(self):
        """Test adding a task with a duplicate name."""
        add_task(self.conn, "Bob", "9876543210")
        result = add_task(self.conn, "Bob", "1234567890")  # Duplicate name
        self.assertEqual(result, "Error: Bob already exists.")

    def test_add_task_invalid_name(self):
        """Test adding a task with an empty name."""
        result = add_task(self.conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_number(self):
        """Test adding a task with an invalid phone number."""
        result = add_task(self.conn, "Charlie", "123456789")  # Incorrect length
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    # Add more test cases for update_task, delete_task, view_all_tasks, etc.


if __name__ == '__main__':
    unittest.main()