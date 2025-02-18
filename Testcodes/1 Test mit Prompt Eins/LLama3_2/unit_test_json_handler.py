import unittest
from json_handler import JSONHandler # Importing the class we want to test

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.file_path = "./JSON-Handler/test.json"
        os.makedirs("./JSON-Handler/", exist_ok=True)
        with open(self.file_path, "w") as file:
            json.dump({"records": []}, file)

    def tearDown(self):
        import shutil
        shutil.rmtree("./JSON-Handler/")

    # Test initialization
    def test_init(self):
        handler = JSONHandler(self.file_path)
        self.assertEqual(handler.file_path, self.file_path)
        self.assertEqual(len(handler.data["records"]), 0)

    # Test loading data from file
    def test_load_data_from_file(self):
        with open(self.file_path, "w") as file:
            json.dump({"records": [{"id": 1, "name": "John"}]}, file)
        handler = JSONHandler(self.file_path)
        self.assertEqual(len(handler.data["records"]), 1)
        self.assertEqual(handler.data["records"][0]["id"], 1)
        self.assertEqual(handler.data["records"][0]["name"], "John")

    # Test saving data to file
    def test_save_data_to_file(self):
        handler = JSONHandler(self.file_path)
        handler.add_record({"id": 1, "name": "John"})
        with open(self.file_path, "r") as file:
            self.assertEqual(json.load(file), {"records": [{"id": 1, "name": "John"}]})

    # Test adding a record
    def test_add_record(self):
        handler = JSONHandler(self.file_path)
        handler.add_record({"id": 1, "name": "John"})
        self.assertEqual(len(handler.data["records"]), 1)
        self.assertEqual(handler.data["records"][0]["id"], 1)
        self.assertEqual(handler.data["records"][0]["name"], "John")

    # Test deleting a record
    def test_delete_record(self):
        handler = JSONHandler(self.file_path)
        handler.add_record({"id": 1, "name": "John"})
        handler.delete_record(1)
        with open(self.file_path, "r") as file:
            self.assertEqual(json.load(file), {"records": []})

    # Test updating a record
    def test_update_record(self):
        handler = JSONHandler(self.file_path)
        handler.add_record({"id": 1, "name": "John"})
        handler.update_record(1, {"name": "Jane"})
        with open(self.file_path, "r") as file:
            self.assertEqual(json.load(file), {"records": [{"id": 1, "name": "Jane"}]})

    # Test listing records
    def test_list_records(self):
        handler = JSONHandler(self.file_path)
        handler.add_record({"id": 1, "name": "John"})
        handler.add_record({"id": 2, "name": "Jane"})
        self.assertEqual(len(handler.data["records"]), 2)

    # Test exporting data to txt file
    def test_export_to_txt(self):
        handler = JSONHandler("./JSON-Handler/test.txt")
        with open("./JSON-Handler/test.txt", "w") as file:
            for record in [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")

        handler.export_data("./JSON-Handler/test.txt", format="txt")
        with open("./JSON-Handler/test.txt", "r") as file:
            self.assertEqual(file.read(), "id: 1\nname: John\n\nid: 2\nname: Jane\n")

    # Test exporting data to xml file
    def test_export_to_xml(self):
        handler = JSONHandler("./JSON-Handler/test.xml")
        with open("./JSON-Handler/test.xml", "w") as file:
            for record in [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]:
                for key, value in record.items():
                    child = Element(key)
                    child.text = str(value)
                    self.root = self.root if hasattr(self.root, 'root') else Element('Records')
                    self.root.append(child)

        handler.export_data("./JSON-Handler/test.xml", format="xml")
        with open("./JSON-Handler/test.xml", "rb") as file:
            tree = ElementTree(file.readline().decode())
            self.assertEqual(tree.getroot().attrib['id'], 1)
            self.assertEqual(tree.getroot().find(".//name").text, "John")

if __name__ == '__main__':
    unittest.main()