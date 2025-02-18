import unittest
from json_handler import JSONHandler # Import the JSONHandler class from main.py

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.json_handler = JSONHandler("./test_data.json") # Create an instance of JSONHandler with a test file path

    def test_init_valid_input(self):
        """
        Test that the initialize method can handle valid input.
        """
        # Initialize the class
        json_handler = JSONHandler("./test_data.json")
        
        # Assert that the file_path and data are correctly set
        self.assertEqual(json_handler.file_path, "./test_data.json")
        self.assertIsNotNone(json_handler.data)

    def test_init_non_existent_file(self):
        """
        Test that the initialize method can handle a non-existent file.
        """
        # Initialize the class with a non-existent file path
        json_handler = JSONHandler("./non_existent_file.json")

        # Assert that the data is correctly set to an empty dictionary
        self.assertEqual(json_handler.data, {"records": []})

    def test_add_record_valid_input(self):
        """
        Test that the add_record method can handle valid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Add a record to the dataset
        json_handler.add_record({"id": 1, "name": "John", "age": 30})

        # Assert that the record was correctly added to the dataset
        self.assertEqual(json_handler.data["records"][0]["id"], 1)
        self.assertEqual(json_handler.data["records"][0]["name"], "John")
        self.assertEqual(json_handler.data["records"][0]["age"], 30)

    def test_add_record_invalid_input(self):
        """
        Test that the add_record method raises an exception for invalid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Try to add a record with invalid input (non-dictionary)
        with self.assertRaises(TypeError):
            json_handler.add_record("Invalid input")

    def test_delete_record_valid_input(self):
        """
        Test that the delete_record method can handle valid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Add some records to the dataset
        for i in range(5):
            json_handler.add_record({"id": i, "name": f"John{i}", "age": i})

        # Delete a record from the dataset
        json_handler.delete_record(2)

        # Assert that the record was correctly deleted
        self.assertEqual(json_handler.data["records"][0]["id"], 1)
        self.assertEqual(json_handler.data["records"][0]["name"], "John0")
        self.assertEqual(json_handler.data["records"][0]["age"], 0)
        for i in range(5):
            self.assertIn(i, [rec.get("id") for rec in json_handler.data["records"]])

    def test_delete_record_invalid_input(self):
        """
        Test that the delete_record method raises an exception for invalid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Try to delete a record with invalid input (non-integer)
        with self.assertRaises(TypeError):
            json_handler.delete_record("Invalid input")

    def test_update_record_valid_input(self):
        """
        Test that the update_record method can handle valid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Add some records to the dataset
        for i in range(5):
            json_handler.add_record({"id": i, "name": f"John{i}", "age": i})

        # Update a record from the dataset
        json_handler.update_record(2, {"age": 31})

        # Assert that the record was correctly updated
        self.assertEqual(json_handler.data["records"][0]["id"], 1)
        self.assertEqual(json_handler.data["records"][0]["name"], "John0")
        self.assertEqual(json_handler.data["records"][0]["age"], 31)

    def test_update_record_invalid_input(self):
        """
        Test that the update_record method raises an exception for invalid input.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Try to update a record with invalid input (non-dictionary)
        with self.assertRaises(TypeError):
            json_handler.update_record(2, "Invalid input")

    def test_list_records(self):
        """
        Test that the list_records method returns an empty list when no records are in the dataset.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Assert that the list of records is correct
        self.assertEqual(json_handler.data["records"], [])

    def test_list_records_valid_input(self):
        """
        Test that the list_records method returns the correct list of records.
        """
        # Create a new JSONHandler instance
        json_handler = JSONHandler("./test_data.json")

        # Add some records to the dataset
        for i in range(5):
            json_handler.add_record({"id": i, "name": f"John{i}", "age": i})

        # Assert that the list of records is correct
        self.assertEqual(json_handler.data["records"], [{"id": 0, "name": "John0", "age": 0}, {"id": 1, "name": "John1", "age": 1}, {"id": 2, "name": "John2", "age": 2}, {"id": 3, "name": "John3", "age": 3}, {"id": 4, "name": "John4", "age": 4}])

if __name__ == '__main__':
    unittest.main()