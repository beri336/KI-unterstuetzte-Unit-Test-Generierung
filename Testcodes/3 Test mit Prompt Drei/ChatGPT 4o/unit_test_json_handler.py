import unittest
import os
import json
from your_module import JSONHandler

class TestJSONHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment: Create a directory for test files."""
        cls.test_dir = "./test_data"
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment: Remove test directory and files."""
        for file in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, file))
        os.rmdir(cls.test_dir)

    def setUp(self):
        """Prepare a fresh JSON handler for each test."""
        self.file_path = os.path.join(self.test_dir, "test.json")
        self.handler = JSONHandler(self.file_path)

    def tearDown(self):
        """Remove the JSON file after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # Positive Test Cases
    def test_add_record(self):
        """Test adding a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.save_data()

        with open(self.file_path, "r") as file:
            data = json.load(file)
        self.assertIn(record, data["records"])

    def test_delete_record(self):
        """Test deleting a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.delete_record(1)
        self.assertNotIn(record, self.handler.data["records"])

    def test_update_record(self):
        """Test updating a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.update_record(1, {"name": "Jane Doe"})
        updated_record = next(rec for rec in self.handler.data["records"] if rec["id"] == 1)
        self.assertEqual(updated_record["name"], "Jane Doe")

    def test_list_records(self):
        """Test listing records."""
        record1 = {"id": 1, "name": "John Doe"}
        record2 = {"id": 2, "name": "Jane Doe"}
        self.handler.add_record(record1)
        self.handler.add_record(record2)
        records = self.handler.list_records()
        self.assertIn(record1, self.handler.data["records"])
        self.assertIn(record2, self.handler.data["records"])

    def test_export_to_txt(self):
        """Test exporting to TXT."""
        export_path = os.path.join(self.test_dir, "test.txt")
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.export_data(export_path, format="txt")
        self.assertTrue(os.path.exists(export_path))

    def test_export_to_xml(self):
        """Test exporting to XML."""
        export_path = os.path.join(self.test_dir, "test.xml")
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.export_data(export_path, format="xml")
        self.assertTrue(os.path.exists(export_path))

    # Edge Cases
    def test_empty_file_creation(self):
        """Test creating a new file when none exists."""
        self.assertFalse(os.path.exists(self.file_path))
        self.handler._load_data()
        self.assertEqual(self.handler.data, {"records": []})

    def test_invalid_json_format(self):
        """Test handling invalid JSON format."""
        with open(self.file_path, "w") as file:
            file.write("{invalid json}")
        data = self.handler._load_data()
        self.assertEqual(data, {"records": []})

    def test_update_nonexistent_record(self):
        """Test updating a record that doesn't exist."""
        self.handler.update_record(1, {"name": "Jane Doe"})
        self.assertNotIn({"id": 1, "name": "Jane Doe"}, self.handler.data["records"])

    def test_delete_nonexistent_record(self):
        """Test deleting a record that doesn't exist."""
        self.handler.delete_record(999)
        self.assertEqual(len(self.handler.data["records"]), 0)

    # Negative Cases
    def test_add_record_without_id(self):
        """Test adding a record without an ID."""
        record = {"name": "John Doe"}
        self.handler.add_record(record)
        self.assertIn(record, self.handler.data["records"])

    def test_export_to_invalid_format(self):
        """Test exporting to an unsupported format."""
        export_path = os.path.join(self.test_dir, "test.invalid")
        self.handler.export_data(export_path, format="invalid")
        self.assertFalse(os.path.exists(export_path))

    # Performance Test Case
    def test_large_number_of_records(self):
        """Test handling a large number of records."""
        for i in range(1000):
            self.handler.add_record({"id": i, "name": f"User{i}"})
        self.handler.save_data()

        with open(self.file_path, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data["records"]), 1000)

if __name__ == "__main__":
    unittest.main()