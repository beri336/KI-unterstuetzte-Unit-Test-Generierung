import unittest
import sqlite3
from your_module import *  # Import your module here

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Sets up a test database for each test case."""
        global list_of_names 
        list_of_names = [] # Reset the global list of names before each test
        database = r"./test_address_book.db"  # Use a separate test database
        self.conn = create_database_file(database)
        self.assertTrue(self.conn is not None, "Database connection failed")
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Cleans up the test database after each test case."""
        reset_all_tasks(self.conn)  
        self.conn.close()

    # Positive Cases 
    def test_create_database_success(self):
        self.assertTrue(os.path.exists("./test_address_book.db"))

    def test_add_task_success(self):
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_update_task_success(self):
        add_task(self.conn, "Bob", "9876543210")
        result = update_task(self.conn, "Bob", "1111111111")
        self.assertEqual(result, "Bob updated successfully.")

    def test_delete_task_success(self):
        add_task(self.conn, "Charlie", "2222222222")
        result = delete_task(self.conn, "Charlie")
        self.assertEqual(result, "Charlie deleted successfully.")

    # Edge Cases
    def test_add_task_duplicate_name(self):
        add_task(self.conn, "David", "3333333333")
        result = add_task(self.conn, "David", "4444444444")
        self.assertEqual(result, "Error: David already exists.")

    def test_add_task_empty_name(self):
        result = add_task(self.conn, "", "5555555555")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_number(self):
        result = add_task(self.conn, "Emily", "1234567")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    # Negative Cases (Should raise exceptions)
    def test_create_database_file_already_exists(self):  
        conn = create_database_file(r"./test_address_book.db")  
        with self.assertRaises(sqlite3.Error) as e: # Use an AssertRaises to check for errors
            create_database_file(r"./test_address_book.db") 

    def test_add_task_connection_error(self):
        # Simulate a database connection error
        with self.assertRaises(sqlite3.Error) as e: 
            conn = sqlite3.connect(":memory:")
            conn.close()  
            add_task(conn, "Fake Name", "1234567890") 

if __name__ == "__main__":
    unittest.main()