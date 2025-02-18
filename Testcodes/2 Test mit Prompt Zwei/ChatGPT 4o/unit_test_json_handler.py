import unittest
import os
import json
from your_script_name import JSONHandler

class TestJSONHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup paths for testing."""
        cls.test_json_file = "./test_records.json"
        cls.test_export_txt = "./test_export.txt"
        cls.test_export_xml = "./test_export.xml"

    def setUp(self):
        """Initialize a fresh JSONHandler before each test."""
        self.handler = JSONHandler(self.test_json_file)
        self.handler.data = {"records": []}  # Reset data
        self.handler.save_data()

    def tearDown(self):
        """Clean up files after each test."""
        for file_path in [self.test_json_file, self.test_export_txt, self.test_export_xml]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_add_record(self):
        """Test adding a record."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.handler.add_record(record)
        self.assertIn(record, self.handler.data["records"])

    def test_delete_record(self):
        """Test deleting a record by ID."""
        record = {"id": 1, "name": "Alice"}
        self.handler.add_record(record)
        self.handler.delete_record(1)
        self.assertNotIn(record, self.handler.data["records"])

    def test_delete_nonexistent_record(self):
        """Test deleting a record that does not exist."""
        initial_count = len(self.handler.data["records"])
        self.handler.delete_record(999)
        self.assertEqual(len(self.handler.data["records"]), initial_count)

    def test_update_record(self):
        """Test updating a record."""
        record = {"id": 1, "name": "Alice"}
        self.handler.add_record(record)
        self.handler.update_record(1, {"name": "Alice Updated"})
        self.assertEqual(self.handler.data["records"][0]["name"], "Alice Updated")

    def test_update_nonexistent_record(self):
        """Test updating a record that does not exist."""
        self.handler.update_record(999, {"name": "Nonexistent"})
        self.assertEqual(len(self.handler.data["records"]), 0)

    def test_list_records(self):
        """Test listing all records."""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        for record in records:
            self.handler.add_record(record)
        with self.assertLogs() as log:
            self.handler.list_records()
            for record in records:
                self.assertIn(str(record), log.output)

    def test_export_to_txt(self):
        """Test exporting data to TXT format."""
        record = {"id": 1, "name": "Alice"}
        self.handler.add_record(record)
        self.handler.export_data(self.test_export_txt, format="txt")
        self.assertTrue(os.path.exists(self.test_export_txt))
        with open(self.test_export_txt, "r") as file:
            content = file.read()
        self.assertIn("id: 1", content)
        self.assertIn("name: Alice", content)

    def test_export_to_xml(self):
        """Test exporting data to XML format."""
        record = {"id": 1, "name": "Alice"}
        self.handler.add_record(record)
        self.handler.export_data(self.test_export_xml, format="xml")
        self.assertTrue(os.path.exists(self.test_export_xml))
        with open(self.test_export_xml, "r") as file:
            content = file.read()
        self.assertIn("<id>1</id>", content)
        self.assertIn("<name>Alice</name>", content)

    def test_invalid_export_format(self):
        """Test exporting with an unsupported format."""
        with self.assertLogs() as log:
            self.handler.export_data(self.test_export_txt, format="csv")
            self.assertIn("Unsupported format", log.output[0])

    def test_load_invalid_json(self):
        """Test loading from an invalid JSON file."""
        with open(self.test_json_file, "w") as file:
            file.write("INVALID JSON")
        handler = JSONHandler(self.test_json_file)
        self.assertEqual(handler.data, {"records": []})

    def test_load_missing_file(self):
        """Test initializing the handler with a missing file."""
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)
        handler = JSONHandler(self.test_json_file)
        self.assertEqual(handler.data, {"records": []})

if __name__ == "__main__":
    unittest.main()