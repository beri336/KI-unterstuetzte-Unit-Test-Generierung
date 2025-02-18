import unittest
import os
import json
from json_handler import JSONHandler


class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        """Set up a temporary JSON file for testing."""
        self.file_path = "./test_data.json"
        self.json_handler = JSONHandler(self.file_path)
        self.json_handler.data = {"records": []}  # Start with empty data
        self.json_handler.save_data()

    def tearDown(self):
        """Clean up by removing the temporary JSON file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # Normal Input Cases
    def test_add_record(self):
        """Test adding a normal record."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.assertIn(record, self.json_handler.data["records"])

    def test_delete_record(self):
        """Test deleting a record by ID."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.delete_record(1)
        self.assertNotIn(record, self.json_handler.data["records"])

    def test_update_record(self):
        """Test updating a record by ID."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        updates = {"email": "alice_new@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.update_record(1, updates)
        updated_record = next(rec for rec in self.json_handler.data["records"] if rec["id"] == 1)
        self.assertEqual(updated_record["email"], "alice_new@example.com")

    def test_list_records(self):
        """Test listing all records."""
        records = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
        for record in records:
            self.json_handler.add_record(record)
        listed_records = self.json_handler.data["records"]
        self.assertEqual(listed_records, records)

    def test_export_to_txt(self):
        """Test exporting records to a TXT file."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        export_path = "./test_data.txt"
        self.json_handler.export_data(export_path, format="txt")
        self.assertTrue(os.path.exists(export_path))
        os.remove(export_path)

    def test_export_to_xml(self):
        """Test exporting records to an XML file."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        export_path = "./test_data.xml"
        self.json_handler.export_data(export_path, format="xml")
        self.assertTrue(os.path.exists(export_path))
        os.remove(export_path)

    # Edge Cases
    def test_add_empty_record(self):
        """Test adding an empty record."""
        record = {}
        self.json_handler.add_record(record)
        self.assertIn(record, self.json_handler.data["records"])

    def test_delete_nonexistent_record(self):
        """Test deleting a record that does not exist."""
        initial_count = len(self.json_handler.data["records"])
        self.json_handler.delete_record(999)  # Nonexistent ID
        self.assertEqual(len(self.json_handler.data["records"]), initial_count)

    def test_update_nonexistent_record(self):
        """Test updating a record that does not exist."""
        updates = {"email": "new_email@example.com"}
        self.json_handler.update_record(999, updates)  # Nonexistent ID
        self.assertNotIn(updates, self.json_handler.data["records"])

    def test_list_records_empty(self):
        """Test listing records when no records exist."""
        listed_records = self.json_handler.data["records"]
        self.assertEqual(listed_records, [])

    # Invalid Input Cases
    def test_invalid_file_path(self):
        """Test initializing with an invalid file path."""
        invalid_path = "/invalid_path/test.json"
        handler = JSONHandler(invalid_path)
        self.assertEqual(handler.data, {"records": []})

    def test_export_invalid_format(self):
        """Test exporting data in an unsupported format."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.export_data("./test_data.unsupported", format="unsupported")
        self.assertFalse(os.path.exists("./test_data.unsupported"))

    def test_non_dict_record(self):
        """Test adding a record that is not a dictionary."""
        with self.assertRaises(AttributeError):  # .get() is called on record
            self.json_handler.add_record(["not", "a", "dict"])

if __name__ == "__main__":
    unittest.main()