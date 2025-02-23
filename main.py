from gui import GenUnitApp # Import the GUI application
from core import TestGenerator # Import the test generation logic

if __name__ == "__main__":
    app = GenUnitApp(None) # Created GUI, but TestGenerator is still missing
    test_generator = TestGenerator(app) # Passes GUI to TestGenerator
    app.test_generator = test_generator # Connects the GUI to the logic
    app.mainloop()
