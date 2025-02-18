import unittest
import os
import json
from json_handler import JSONHandler

class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_records.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.handler = JSONHandler(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_data_new_file(self):
        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})

    def test_load_data_invalid_json(self):
        with open(self.test_file, "w") as file:
            file.write("{invalid json}")

        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})

    def test_save_data(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.save_data()

        with open(self.test_file, "r") as file:
            data = json.load(file)

        self.assertEqual(data, {"records": [{"id": 1, "name": "Alice"}]})

    def test_add_record(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_delete_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(1)
        self.assertEqual(self.handler.data["records"], [])

    def test_delete_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(2)
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_update_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(1, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Bob"}])

    def test_update_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(2, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_list_records(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.add_record({"id": 2, "name": "Bob"})
        records = self.handler.data["records"]
        self.assertEqual(records, [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])

    def test_export_to_txt(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        txt_file = "test_export.txt"
        self.handler.export_data(txt_file, format="txt")
        
        with open(txt_file, "r") as file:
            content = file.read()
        
        self.assertIn("id: 1", content)
        self.assertIn("name: Alice", content)

        os.remove(txt_file)

    def test_export_to_xml(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        xml_file = "test_export.xml"
        self.handler.export_data(xml_file, format="xml")
        
        with open(xml_file, "r") as file:
            content = file.read()
        
        self.assertIn("<id>1</id>", content)
        self.assertIn("<name>Alice</name>", content)

        os.remove(xml_file)

    def test_export_data_invalid_format(self):
        with self.assertLogs(level="INFO") as log:
           

 self.handler.export_data("test_file", format="unsupported")
        self.assertIn("Unsupported format", log.output[0])