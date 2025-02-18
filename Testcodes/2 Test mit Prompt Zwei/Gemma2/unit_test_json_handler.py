import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# Import your JSONHandler class (replace 'JSONHandler' with the actual name) from the same directory
from JSONHandler import JSONHandler 

def test_json_handler():
    """Tests the functionality of the JSONHandler class."""

    # Test Case: Initialization and Loading Data
    handler = JSONHandler("./test.json")  # Create a handler with a temporary file
    assert handler.data == {"records": []}, "Initial data should be an empty list"

    # Test Case: Saving Data to File
    handler.add_record({"id": 1, "name": "Alice"})
    handler.save_data()  

    # Reload the data from the file after saving
    loaded_handler = JSONHandler("./test.json") 
    assert len(loaded_handler.data["records"]) == 1, "Data should be saved and loaded correctly"

    # Test Case: Adding Records
    handler.add_record({"id": 2, "name": "Bob"})
    handler.save_data() 
    loaded_handler = JSONHandler("./test.json")  
    assert len(loaded_handler.data["records"]) == 2, "Records should be added successfully"

    # Test Case: Deleting Records by ID
    handler.delete_record(1)
    handler.save_data() 
    loaded_handler = JSONHandler("./test.json")  
    assert len(loaded_handler.data["records"]) == 1, "Record should be deleted correctly"

    # Test Case: Updating Records by ID
    handler.update_record(2, {"name": "Bobby"})
    handler.save_data()
    loaded_handler = JSONHandler("./test.json")
    assert loaded_handler.data["records"][0]["name"] == "Bobby", "Record should be updated correctly"

    # Test Case: Listing Records 
    handler.list_records()  
    # Output should display the single record (record with ID 2)

    # Special Cases and Edge Cases

    # 1. Handling Missing File: Ensure that a new file is created if the specified path doesn't exist.
    os.remove("./test.json")
    handler = JSONHandler("./test.json")  
    assert len(handler.data["records"]) == 0, "A new file should be created when the file doesn't exist"

    # 2. Invalid JSON: Test what happens when a corrupted JSON file is loaded (consider using `JSONDecodeError`).

    # 3. Exporting to TXT and XML
    handler.export_data("./test_export.txt")  # Export to TXT
    handler.export_data("./test_export.xml", format="xml") # Export to XML



if __name__ == "__main__":
    test_json_handler() 