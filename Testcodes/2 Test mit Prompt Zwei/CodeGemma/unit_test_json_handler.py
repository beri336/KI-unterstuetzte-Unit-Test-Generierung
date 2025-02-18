import json
import os
import unittest

from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

path = "./JSON-Handler/" # path to save all files

class JSONHandlerTest(unittest.TestCase):

    def setUp(self):
        self.file_path = os.path.join(path, "test.json")
        self.handler = JSONHandler(self.file_path)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_load_data(self):
        self.assertEqual(self.handler.data, {"records": []})

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
        self.handler.export_data(os.path.join(path, "test.txt"), "txt")
        self.assertTrue(os.path.exists(os.path.join(path, "test.txt")))

    def test_export_to_xml(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.export_data(os.path.join(path, "test.xml"), "xml")
        self.assertTrue(os.path.exists(os.path.join(path, "test.xml")))

if __name__ == "__main__":
    unittest.main()