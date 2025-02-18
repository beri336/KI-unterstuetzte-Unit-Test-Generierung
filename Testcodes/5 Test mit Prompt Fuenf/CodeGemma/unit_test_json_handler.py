import unittest
from main import JSONHandler

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.json_handler = JSONHandler("test_data.json")

    def test_add_record(self):
        """Test adding a new record."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.assertEqual(len(self.json_handler.data["records"]), 1)

    def test_delete_record(self):
        """Test deleting a record."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.json_handler.delete_record(1)
        self.assertEqual(len(self.json_handler.data["records"]), 0)

    def test_update_record(self):
        """Test updating a record."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.json_handler.update_record(1, {"name": "Jane Doe"})
        self.assertEqual(self.json_handler.data["records"][0]["name"], "Jane Doe")

    def test_list_records(self):
        """Test listing all records."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.json_handler.add_record({"id": 2, "name": "Jane Doe"})
        self.assertEqual(len(self.json_handler.list_records()), 2)

    def test_export_to_txt(self):
        """Test exporting data to TXT format."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.json_handler.export_data("test_output.txt", "txt")
        self.assertTrue(os.path.exists("test_output.txt"))

    def test_export_to_xml(self):
        """Test exporting data to XML format."""
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.json_handler.export_data("test_output.xml", "xml")
        self.assertTrue(os.path.exists("test_output.xml"))

if __name__ == "__main__":
    unittest.main()