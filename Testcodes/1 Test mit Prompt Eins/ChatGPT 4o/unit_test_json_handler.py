import unittest
import os
import json
from your_module import JSONHandler

class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        """Set up a temporary JSON file for testing."""
        self.test_file_path = "./test_data.json"
        self.handler = JSONHandler(self.test_file_path)

    def tearDown(self):
        """Clean up the temporary JSON file after tests."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_initial_load(self):
        """Test loading data from a non-existent file."""
        self.assertEqual(self.handler.data, {"records": []}, "Data should initialize with an empty dataset.")

    def test_add_record(self):
        """Test adding a new record."""
        record = {"id": 1, "name": "Test Record"}
        self.handler.add_record(record)
        self.assertIn(record, self.handler.data["records"], "Record should be added to the dataset.")

    def test_delete_record(self):
        """Test deleting a record by ID."""
        record1 = {"id": 1, "name": "Test Record 1"}
        record2 = {"id": 2, "name": "Test Record 2"}
        self.handler.add_record(record1)
        self.handler.add_record(record2)
        self.handler.delete_record(1)
        self.assertNotIn(record1, self.handler.data["records"], "Record 1 should be deleted.")
        self.assertIn(record2, self.handler.data["records"], "Record 2 should remain in the dataset.")

    def test_update_record(self):
        """Test updating a record by ID."""
        record = {"id": 1, "name": "Old Name"}
        self.handler.add_record(record)
        self.handler.update_record(1, {"name": "New Name"})
        self.assertEqual(self.handler.data["records"][0]["name"], "New Name", "Record name should be updated.")

    def test_list_records(self):
        """Test listing all records."""
        record1 = {"id": 1, "name": "Record 1"}
        record2 = {"id": 2, "name": "Record 2"}
        self.handler.add_record(record1)
        self.handler.add_record(record2)
        with self.assertLogs(level="INFO") as log:
            self.handler.list_records()
        self.assertIn(str(record1), log.output[0], "Record 1 should appear in the list output.")
        self.assertIn(str(record2), log.output[1], "Record 2 should appear in the list output.")

    def test_export_to_txt(self):
        """Test exporting data to a TXT file."""
        record = {"id": 1, "name": "Test Record"}
        self.handler.add_record(record)
        export_path = "./export_test.txt"
        self.handler.export_data(export_path, format="txt")
        self.assertTrue(os.path.exists(export_path), "TXT export file should be created.")
        with open(export_path, "r") as file:
            content = file.read()
        self.assertIn("id: 1", content, "Exported TXT should contain the record ID.")
        self.assertIn("name: Test Record", content, "Exported TXT should contain the record name.")
        os.remove(export_path)

    def test_export_to_xml(self):
        """Test exporting data to an XML file."""
        record = {"id": 1, "name": "Test Record"}
        self.handler.add_record(record)
        export_path = "./export_test.xml"
        self.handler.export_data(export_path, format="xml")
        self.assertTrue(os.path.exists(export_path), "XML export file should be created.")
        with open(export_path, "r") as file:
            content = file.read()
        self.assertIn("<id>1</id>", content, "Exported XML should contain the record ID.")
        self.assertIn("<name>Test Record</name>", content, "Exported XML should contain the record name.")
        os.remove(export_path)

    def test_save_and_load_data(self):
        """Test saving and reloading data."""
        record = {"id": 1, "name": "Persisted Record"}
        self.handler.add_record(record)
        self.handler.save_data()
        new_handler = JSONHandler(self.test_file_path)
        self.assertIn(record, new_handler.data["records"], "Record should persist after saving and loading.")

if __name__ == "__main__":
    unittest.main()