import unittest
from json_handler import JSONHandler

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.handler = JSONHandler("test_data.json")

    def test_load_data_existing_file(self):
        self.assertIsInstance(self.handler.data, dict)

    def test_load_data_non_existing_file(self):
        handler = JSONHandler("non_existent_file.json")
        self.assertEqual(handler.data, {"records": []})

    def test_add_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.assertEqual(len(self.handler.data["records"]), 1)

    def test_delete_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.delete_record(1)
        self.assertEqual(len(self.handler.data["records"]), 0)

    def test_update_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.update_record(1, {"name": "Jane"})
        self.assertEqual(self.handler.data["records"][0]["name"], "Jane")

    def test_export_to_txt(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.export_data("test_export.txt", "txt")
        self.assertTrue(os.path.exists("test_export.txt"))

    def test_export_to_xml(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.export_data("test_export.xml", "xml")
        self.assertTrue(os.path.exists("test_export.xml"))

if __name__ == "__main__":
    unittest.main()