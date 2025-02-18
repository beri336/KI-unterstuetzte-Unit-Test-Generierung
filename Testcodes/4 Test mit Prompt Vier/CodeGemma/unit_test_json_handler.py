import unittest
from main import JSONHandler

class TestJSONHandler(unittest.TestCase):

    def test_init_valid_file(self):
        """Test initializing with a valid JSON file."""
        handler = JSONHandler("valid_file.json")
        self.assertIsNotNone(handler.data)

    def test_init_invalid_file(self):
        """Test initializing with an invalid JSON file."""
        handler = JSONHandler("invalid_file.json")
        self.assertIsNone(handler.data)

    def test_add_record(self):
        """Test adding a record."""
        handler = JSONHandler("test_file.json")
        handler.add_record({"id": 1, "name": "John"})
        self.assertEqual(len(handler.data["records"]), 1)

    def test_delete_record(self):
        """Test deleting a record."""
        handler = JSONHandler("test_file.json")
        handler.add_record({"id": 1, "name": "John"})
        handler.delete_record(1)
        self.assertEqual(len(handler.data["records"]), 0)

    def test_update_record(self):
        """Test updating a record."""
        handler = JSONHandler("test_file.json")
        handler.add_record({"id": 1, "name": "John"})
        handler.update_record(1, {"name": "Jane"})
        self.assertEqual(handler.data["records"][0]["name"], "Jane")

if __name__ == "__main__":
    unittest.main()