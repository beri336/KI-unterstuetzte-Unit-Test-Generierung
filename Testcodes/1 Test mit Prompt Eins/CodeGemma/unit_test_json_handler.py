import unittest
from json_handler import JSONHandler

class JSONHandlerTest(unittest.TestCase):

    def setUp(self):
        self.test_file_path = "test.json"
        self.handler = JSONHandler(self.test_file_path)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_init(self):
        self.assertEqual(self.handler.file_path, self.test_file_path)
        self.assertIsInstance(self.handler.data, dict)

    def test_load_data(self):
        self.handler._load_data()
        self.assertEqual(self.handler.data, {"records": []})

    def test_save_data(self):
        self.handler.save_data()
        self.assertTrue(os.path.exists(self.test_file_path))

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

    def test_list_records(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.list_records()

    def test_export_data(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.export_data("test.txt", "txt")
        self.assertTrue(os.path.exists("test.txt"))

if __name__ == "__main__":
    unittest.main()