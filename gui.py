import customtkinter as ctk # GUI framework
import threading # For running test generation in a separate thread
import psutil # Check if Ollama is running
import os # File and folder operations
from tkinter import filedialog # Open file/folder selection dialogs
from helpers import fetch_models, output_terminal # Load AI models & terminal logging

class GenUnitApp(ctk.CTk):
    '''
    A GUI application for the automated generation of unit tests using AI.
    
    This class creates a user interface with 'customtkinter',
    in which users:
    - Select a project folder with Python files
    - Load a prompt file for test generation
    - Select an AI model for test generation
    - Start the generation and track the progress

    The class connects the UI with the core logic ('TestGenerator')
    and handles status management and user interactions.
    '''
    def __init__(self, test_generator):
        ''' 
        Initializes the main GUI application and sets all required variables.

        This method:
        - Connects the user interface to the core logic ('TestGenerator')
        - Defines local properties to manage paths, models & UI elements
        - Creates the GUI through 'create_widgets()'
        - Checks the status of the Ollama service

        Parameters:
        - test_generator (TestGenerator): Instance of the core logic for test generation.
        '''
        super().__init__()
        self.test_generator = test_generator # Reference to core logic

        # Local properties (instead of global variables)
        self.folder_path = None
        self.prompt_file_path = None
        self.excluded_folder_path = None
        self.selected_model = "None"

        # UI elements (are created in `create_widgets()`)
        self.ollama_status_label = None
        self.status_label = None
        self.generate_label = None
        self.btn_generate = None
        self.btn_exclude_folder = None
        self.btn_folder = None
        self.btn_prompt_file = None
        self.tb_chosen_folder = None
        self.tb_chosen_prompt_file = None
        self.tb_excluded_folder = None
        self.checkbox_save_raw = None
        self.checkbox_create_log = None
        self.combo_models = None
        self.progress_bar = None

        self.is_generating_tests = False
        self.generation_thread = None
        self.model_list = None

        # Build GUI
        self.create_widgets()
        self.check_ollama_status()

    def create_widgets(self):
        '''
        Creates and configures all UI elements for the application.

        This method:
        - Sets the appearance and window size
        - Creates various UI areas, including:
            - Status labels to display progress & connection status
            - Selection options for folders, folders to exclude and prompt files
            - A drop-down menu to select an AI model
            - Additional options for markdown storage and logging
            - A progress bar for the test generation process
        - Initializes the 'check_ollama_status()' method to check the Ollama status
        '''
        # Sets design mode and color scheme
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        
        # Main window settings
        self.geometry("600x710")
        self.minsize(600, 710)
        self.maxsize(600, 710)
        self.title("Unit Test-Generation with AI [GenUnit]")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Main frame for UI elements
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Status frame
        frame_label = ctk.CTkFrame(main_frame)
        frame_label.pack(padx=10, pady=10, fill="x")
        frame_label.columnconfigure((0, 1, 2), weight=1)

        # Status labels
        self.generate_label = ctk.CTkLabel(frame_label, text="Ready", text_color="green", font=("Arial", 14))
        self.generate_label.grid(row=0, column=0, sticky="w", padx=4)

        self.status_label = ctk.CTkLabel(frame_label, text="OK", text_color="green", font=("Arial", 14))
        self.status_label.grid(row=0, column=1, sticky="n", padx=4)

        self.ollama_status_label = ctk.CTkLabel(frame_label, text="Checking...", text_color="orange", font=("Arial", 14))
        self.ollama_status_label.grid(row=0, column=2, sticky="e", padx=4)

        # Folder selection
        frame_select_folder = ctk.CTkFrame(main_frame)
        frame_select_folder.pack(padx=10, pady=10, fill="x")

        lbl_chosen_folder = ctk.CTkLabel(frame_select_folder, text="Selected Folder:", font=("Arial", 14))
        lbl_chosen_folder.pack(pady=4, anchor="w", padx=4)

        self.tb_chosen_folder = ctk.CTkTextbox(frame_select_folder, height=30, state="disabled")
        self.tb_chosen_folder.pack(side="left", padx=4, pady=4, expand=True, fill="x")

        self.btn_folder = ctk.CTkButton(frame_select_folder, text="Choose Folder", command=self.choose_folder)
        self.btn_folder.pack(side="left", padx=5, pady=4)

        # Exclude a subfolder
        frame_exclude_folder = ctk.CTkFrame(main_frame)
        frame_exclude_folder.pack(padx=10, pady=10, fill="x")

        lbl_excluded_folder = ctk.CTkLabel(frame_exclude_folder, text="Excluded Folder:", font=("Arial", 14))
        lbl_excluded_folder.pack(pady=4, anchor="w", padx=4)

        self.tb_excluded_folder = ctk.CTkTextbox(frame_exclude_folder, height=30, state="disabled")
        self.tb_excluded_folder.pack(side="left", padx=4, pady=4, expand=True, fill="x")

        self.btn_exclude_folder = ctk.CTkButton(frame_exclude_folder, text="Choose Excluded Folder", command=self.choose_exclude_folder, state="disabled")
        self.btn_exclude_folder.pack(side="left", padx=5, pady=4)

        # Select prompt file
        frame_prompt = ctk.CTkFrame(main_frame)
        frame_prompt.pack(padx=10, pady=10, fill="x")

        lbl_chosen_prompt_file = ctk.CTkLabel(frame_prompt, text="Prompt File:", font=("Arial", 14))
        lbl_chosen_prompt_file.pack(pady=4, anchor="w", padx=4)

        self.tb_chosen_prompt_file = ctk.CTkTextbox(frame_prompt, height=100)
        self.tb_chosen_prompt_file.pack(side="left", padx=4, pady=4, expand=True, fill="x")

        self.btn_prompt_file = ctk.CTkButton(frame_prompt, text="Choose Prompt File", command=self.choose_prompt_file)
        self.btn_prompt_file.pack(side="left", padx=5, pady=4)

        # AI model selection
        frame_model_selection = ctk.CTkFrame(main_frame)
        frame_model_selection.pack(padx=10, pady=10, fill="x")

        lbl_model_select = ctk.CTkLabel(frame_model_selection, text=" Select AI Model:", font=("Arial", 14))
        lbl_model_select.grid(row=0, column=0, padx=(0, 10), pady=4, sticky="w")

        #self.model_list = fetch_models()
        self.model_list = fetch_models(self)

        self.combo_models = ctk.CTkComboBox(frame_model_selection, values=self.model_list, command=self.on_model_select, width=300)
        self.combo_models.grid(row=0, column=1, padx=0, pady=4, sticky="w")
        self.combo_models.set("None")

        # Additional options
        frame_generate = ctk.CTkFrame(main_frame)
        frame_generate.pack(padx=10, pady=10, fill="x")

        self.checkbox_save_raw = ctk.CTkCheckBox(frame_generate, text="Save Raw Markdown")
        self.checkbox_save_raw.pack(side="top", pady=4)
        self.checkbox_save_raw.select() # Activated by default

        self.checkbox_create_log = ctk.CTkCheckBox(frame_generate, text="Create Log-File")
        self.checkbox_create_log.pack(side="top", pady=4)
        self.checkbox_create_log.select() # Activated by default

        # Start test generation
        self.btn_generate = ctk.CTkButton(frame_generate, text="Generate", command=self.start_test_generation)
        self.btn_generate.pack(side="top", pady=4)

        # Progress bar
        frame_progress = ctk.CTkFrame(main_frame)
        frame_progress.pack(padx=10, pady=10, fill="x")

        self.progress_bar = ctk.CTkProgressBar(frame_progress, orientation="horizontal", width=400, mode="determinate")
        self.progress_bar.pack(pady=10, anchor="center")
        self.progress_bar.set(0.0)

        # Footer with trademark & disclaimer
        trademark_label = ctk.CTkLabel(main_frame, text="© 2025 Created by Berkant - GenUnit", font=("Arial", 10))
        trademark_label.pack(pady=5, anchor="center")

        disclaimer_label = ctk.CTkLabel(main_frame, text="Use at your own risk.", font=("Arial", 10), text_color="red")
        disclaimer_label.pack(pady=5, anchor="center")

        self.check_ollama_status()

    # Selection functions
    def choose_folder(self):
        '''
        Opens a dialog to select a project folder and updates the UI accordingly.

        This method:
        - Opens a dialog box for folder selection ('filedialog.askdirectory()')
        - If no folder is selected, the action is canceled
        - Displays the selected folder in a text field of the UI
        - Activates the button to exclude subfolders
        - Automatically searches for a prompt file ('prompt.txt', 'prompt.md', 'prompt.doc') in the selected folder:
            - If found, it will be loaded and displayed in the UI text field
            - If not found, a warning is issued
        - Outputs corresponding status messages in the terminal
        '''
        self.folder_path = filedialog.askdirectory(title="Choose a Folder with Python Files")

        # If no folder was selected, cancel
        if not self.folder_path:
            output_terminal("Warning #5: No folder selected.", "bg_yellow")
            return

        # Show the selected folder in the UI text field
        self.tb_chosen_folder.configure(state="normal")
        self.tb_chosen_folder.delete("1.0", ctk.END)
        self.tb_chosen_folder.insert("1.0", self.folder_path)
        self.tb_chosen_folder.configure(state="disabled")

        # Activate the button to exclude subfolders
        self.btn_exclude_folder.configure(state="normal")

        # Search for a prompt file (`prompt.txt`, `prompt.md`, `prompt.doc`) in the selected folder
        self.prompt_file_path = None
        for ext in ["txt", "md", "doc"]: # File format list
            potential_path = os.path.join(self.folder_path, f"prompt.{ext}")
            if os.path.exists(potential_path):
                self.prompt_file_path = potential_path
                break # Erste gefundene Datei verwenden

        # If a prompt file was found, load it into the prompt text field
        if self.prompt_file_path:
            try:
                with open(self.prompt_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read().strip() # Remove space at the beginning/end

                # Ensure that `self.tb_chosen_prompt_file` exists
                if hasattr(self, 'tb_chosen_prompt_file') and self.tb_chosen_prompt_file:
                    self.tb_chosen_prompt_file.configure(state="normal")
                    self.tb_chosen_prompt_file.delete("1.0", ctk.END)
                    self.tb_chosen_prompt_file.insert("1.0", file_content)
                    self.tb_chosen_prompt_file.configure(state="disabled")

                # Success message in the terminal
                output_terminal(f"Info #19: Automatically found prompt file: '{os.path.basename(self.prompt_file_path)}'", "yellow")

            except Exception as e:
                # Error handling if the file cannot be read
                output_terminal(f"Error #11: Could not read prompt file - {e}", "red")
        
        else:
            # If no prompt file was found
            output_terminal("Warning #6: No prompt file found in the selected folder.", "bg_yellow")

        # Confirm successful selection in the terminal and GUI
        output_terminal(f"Info #20: Your selected folder: '{self.folder_path}'", "yellow")

    def choose_exclude_folder(self):
        '''
        Opens a dialog for selecting a subfolder to be excluded and validates the selection.

        This method:
        - Checks whether a main folder has already been selected (otherwise an error message is displayed)
        - Opens a dialog box for folder selection ('filedialog.askdirectory()')
        - If a folder has been selected:
            - Checks whether the selected folder is inside the main folder
            - If yes: Saves it as 'self.excluded_folder_path' and updates the UI text field
            - If not: Displays an error message and discards the selection
        - If the user closes the dialog without making a selection, the UI text field is cleared
        - Outputs corresponding status messages in the terminal
        '''
        # Check whether a main folder has been selected
        if not self.folder_path:
            output_terminal(f"Error #9: No main folder selected. Please choose a main folder first.", "bg_red")
            return
        
        # If an exclusion folder already exists, open the dialog there - otherwise in the main folder
        start_path = self.excluded_folder_path if self.excluded_folder_path else self.folder_path

        # Open the file dialog for the folder selection
        self.excluded_folder_path = filedialog.askdirectory(title="Choose a Subfolder to Exclude", initialdir=start_path)

        # If the user cancels the selection, empty the text field and display a message
        if not self.excluded_folder_path:
            output_terminal("Info #17: Folder exclusion was cancelled.", "yellow")
            self.tb_excluded_folder.configure(state="normal") # Unlock text box so that we can change the text
            self.tb_excluded_folder.delete("1.0", ctk.END) # Delete text box content
            self.tb_excluded_folder.configure(state="disabled") # Deactivate text box again
            return # Exit function so that no error message appears
        
        # Check whether the selected folder is within the main folder
        try:
            rel_path = os.path.relpath(self.excluded_folder_path, self.folder_path)
            if rel_path.startswith(".."):
                raise ValueError("Selected folder is not a subfolder!")

            # Valid subfolder -> Update text field
            self.tb_excluded_folder.configure(state="normal")
            self.tb_excluded_folder.delete("1.0", ctk.END)
            self.tb_excluded_folder.insert("1.0", self.excluded_folder_path)
            self.tb_excluded_folder.configure(state="disabled")
            output_terminal(f"Info #18: Excluded folder: '{self.excluded_folder_path}'", "yellow")

        except ValueError:
            # Error message if the folder is not within the main folder
            output_terminal("Error #10: The excluded folder must be a subfolder of the main folder.", "bg_red")
            self.excluded_folder_path = None

    def choose_prompt_file(self):
        '''
        Opens a file dialog to select a prompt file and loads the content into the UI.

        This method:
        - Opens a file selection dialog box ('filedialog.askopenfilename()')
        - If the user does not select a file, the action is canceled
        - If a file has been selected:
            - The content is read and displayed in the UI text field ('tb_chosen_prompt_file')
            - The text field is first unlocked, then deactivated again (read-only)
        - Outputs a success message in the terminal when the file has been successfully loaded
        - If an error occurs (e.g. file cannot be opened), an error message is displayed
        '''
        try:
            # Open file dialog to select a prompt file
            self.prompt_file_path = filedialog.askopenfilename(
                title="Choose Your Prompt File",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )

            # If no file was selected, cancel
            if not self.prompt_file_path:
                output_terminal("Warning #4: No prompt file selected.", "bg_yellow")
                return

            # Open file and read content
            with open(self.prompt_file_path, 'r', encoding='utf-8') as file:
                file_content = file.read().strip()

            # Update text field (first unlock, then lock)
            self.tb_chosen_prompt_file.configure(state="normal")
            self.tb_chosen_prompt_file.delete("1.0", ctk.END)
            self.tb_chosen_prompt_file.insert("1.0", file_content)
            self.tb_chosen_prompt_file.configure(state="disabled")

            output_terminal(f"Info #16: Prompt manually loaded from '{os.path.basename(self.prompt_file_path)}'", "yellow")

        except Exception as e:
            # Error handling if file cannot be opened
            output_terminal(f"Error #8: Could not load prompt file - {e}", "bg_red")

    def on_model_select(self, event):
        '''
        Updates the selected AI model and adjusts the UI accordingly.

        This method:
        - Takes the selected model from the ComboBox or sets the default value 'None'
        - Updates the 'self.selected_model' variable
        - Explicitly sets the value of the ComboBox (prevents errors caused by unexpected events)
        - If 'None' was selected:
            - Resets the 'Generate' button to the default text
            - Outputs an info message in the terminal
        - If a model was selected:
            - Updates the 'Generate' button to update its text with the model name
            - Outputs a confirmation message in the terminal
        - Returns the new button text as a return value
        '''
        # Update `selected_model` with the new value or set “None” as default
        if not event or event.strip() == "":
            self.selected_model = "None"
        else:
            self.selected_model = event.strip()

        # Set the value of the ComboBox explicitly (prevents errors in the event of unexpected events)
        self.combo_models.set(self.selected_model)

        # If “None” was selected, reset the button to the default text
        if self.selected_model == "None":
            self.btn_generate.configure(text="Generate")
            output_terminal("Info #14: No model selected. Please choose an AI model.", "green")
            return "Generate"

        # Update the button text with the selected model
        new_text = f"Generate Unit Test with '{self.selected_model}'"
        self.btn_generate.configure(text=new_text)
        
        output_terminal(f"Info #15: Model selected: '{self.selected_model}'", "yellow")

        return new_text

    def set_ollama_label(self, opt):
        '''
        Updates the label for displaying the Ollama status in the user interface.

        Parameters:
        - opt (str): The new status of Ollama, can be:
            - 'Online' -> Sets the label to 'Ollama Online' (green)
            - 'Offline' -> Sets the label to 'Ollama Offline' (red)
            - All other values -> Sets the label to 'Error' (gray)

        This method:
        - Configures the text and color of the 'ollama_status_label' widget based on 'opt'
        - If the value passed is not 'Online' or 'Offline', 'Error' is set
        '''
        if opt == "Online":
            self.ollama_status_label.configure(text="Ollama Online", text_color="green")
        elif opt == "Offline":
            self.ollama_status_label.configure(text="Ollama Offline", text_color="red")
        else:
            self.ollama_status_label.configure(text="Error", text_color="grey")
            return
    
    # Status and progress
    def set_status_label(self, msg):
        '''
        Updates the status label in the UI with a new message.

        Parameters:
        - msg (str): The new text that will be displayed in the status label.

        This method:
        - Sets the text of the 'status_label' widget to the passed value
        - Uses the color green for the text by default
        '''
        self.status_label.configure(text=msg)

    def set_generate_label(self, msg, color="green"):
        '''
        Updates the label for the test generation status in the UI.

        Parameters:
        - msg (str): The new message describing the current test generation status.
        - color (str, optional): The color of the text (default: "green").

        This method:
        - Sets the text of the 'generate_label' widget to the passed value
        - Uses the color green for the text by default
        '''
        self.generate_label.configure(text=msg, text_color=color)

    def initialize_progress_bar(self, total_files):
        '''
        Initializes the progress bar for the test generation process.

        Parameters:
        - total_files (int): The total number of files to be processed.

        This method:
        - Sets the progress bar ('progress_bar') to 0.0 (initial state)
        - Outputs an info message in the terminal to confirm the initializatio
        '''
        # Reset progress bar
        self.progress_bar.set(0.0)

        output_terminal(f"Info #8: Progress bar initialized for {total_files} files.", "yellow")

    def update_progress_bar(self, completed_tests, total_files):
        '''
        Updates the progress bar based on the completed tests.

        Parameters:
        - completed_tests (int): The number of tests already generated
        - total_files (int): The total number of files to be processed

        This method:
        - Calculates the progress as a ratio of 'completed_tests / total_files'
        - Updates the value of the progress bar ('progress_bar')
        - Outputs a terminal message to indicate progress
        - If 'total_files == 0', a warning is issued to avoid division by zero
        '''
        if total_files == 0: # Prevent division by zero
            output_terminal(f"Warning #3: No files to process, progress bar update skipped.", "bg_yellow")
            return

        progress_value = completed_tests / total_files # Value between 0.0 and 1.0
        self.progress_bar.set(progress_value)

        output_terminal(f"Info #9: Progress: {completed_tests}/{total_files} tests completed ({progress_value*100:.2f}%)", "yellow")

    def reset_progress_bar(self):
        '''Resets the progress bar to the initial state.

        This method:
        - Sets the value of the progress bar ('progress_bar') to 0.0
        - Outputs an info message in the terminal to confirm the reset
        '''
        # Reset progress bar
        self.progress_bar.set(0.0)

        output_terminal(f"Info #10: Progress bar reset.", "yellow")

    # Start test generation
    def start_test_generation(self): # (generate_tests)
        '''
        Starts the test generation process for the selected Python files.

        This method:
        - Checks if a main folder ('folder_path') has been selected
        - Checks if a prompt file ('tb_chosen_prompt_file') is loaded
        - Ensures that an AI model ('selected_model') has been selected
        - Searches for Python files in the specified folder (and excludes subfolders if necessary)
        - If no Python files are found, the process is aborted
        - Displays the number of files found and updates the UI status
        - Initializes the progress bar
        - Deactivates relevant UI elements to prevent changes during generation
        - Starts the test generation in a separate thread to avoid blocking the GUI
        - Tracks the progress of the generation with 'check_generation_completion()'
        '''
        # Check if main folder is selected
        if not self.folder_path:
            output_terminal("Error #1-Please choose a folder.", "bg_red")
            self.set_status_label("Please select a folder.")
            return
        
        # Check if a prompt exists
        if not self.tb_chosen_prompt_file.get("1.0", ctk.END).strip():
            output_terminal("Error #2-No prompt selected.", "bg_red")
            self.set_status_label("Please choose a prompt.")
            return
        
        # Check if an AI model has been selected
        if self.selected_model == "None":
            output_terminal("Error #3-Please select an AI model before generating tests.", "bg_red")
            self.set_status_label("Please choose an AI model.")
            return
        
        output_terminal(f"Info #1-Mardown-Checkbox Status is: {self.checkbox_save_raw.get()}", "green")
        output_terminal(f"Info #2-Log-Checkbox Status is: {self.checkbox_create_log.get()}", "green")

        # Search for Python files in the selected folder
        py_files = self.test_generator.get_python_files(self.folder_path, self.excluded_folder_path)

        # If no Python files were found, end the generation
        if not py_files:
            output_terminal("Warning #1-No Python files found in the selected folder.", "bg_yellow")
            self.set_status_label("No Python files found.")
            return

        # Display the number of files found
        total_files = len(py_files)
        output_terminal(f"Info #3-Found {total_files} Python file(s): {', '.join(os.path.basename(f) for f in py_files)}", "yellow")
        
        # Update status for current generation
        self.set_generate_label("Generation in progress...")
        self.set_status_label(f"Total files found: {total_files}")

        # Initialize the progress bar
        self.initialize_progress_bar(total_files)

        # Start the generation
        self.is_generating_tests = True # Set variable that the generation is running
        self.btn_generate.configure(state="disabled", text="Generating, please wait...")
        self.btn_exclude_folder.configure(state="disabled")
        self.btn_folder.configure(state="disabled")
        self.btn_prompt_file.configure(state="disabled")
        self.combo_models.configure(state="disabled")
        self.checkbox_save_raw.configure(state="disabled")
        self.checkbox_create_log.configure(state="disabled")

        # Start the generation in a separate thread to avoid blocking the GUI
        self.generation_thread = threading.Thread(
            target=self.test_generator.generate_tests_for_folder, 
            args=(self.selected_model, total_files, py_files), 
            daemon=True
        )
        self.generation_thread.start()
        
        # Track the progress of the generation
        self.test_generator.check_generation_completion()

    # Check Ollama status
    def check_ollama_status(self):
        '''
        Checks the current status of the Ollama process and updates the UI accordingly.

        This method:
        - Ensures that all required GUI elements are present
        - Checks whether a process with the name “ollama” is active ('psutil.process_iter()')
        - If Ollama is running:
            - The status label is set to 'Ollama Online'
            - The 'Generate' button is activated (if no generation is running)
        - If Ollama is not running:
            - The status label is set to 'Ollama Offline'
            - The 'Generate' button is deactivated
        - Repeats the check every 5 seconds ('self.after(5000, self.check_ollama_status)')
        - Outputs info or error messages in the terminal if an error occurs
        '''
        # Check whether all GUI elements are present
        if not all([self.ollama_status_label, self.btn_generate, self.generate_label]):
            output_terminal(f"Error #12: Some GUI elements are None! The interface might not be fully initialized.", "red")
            return # If GUI is not ready, cancel

        try:
            # Check whether a process with “ollama” in its name is running
            ollama_running = any("ollama" in (proc.info.get("name", "").lower()) for proc in psutil.process_iter(["name"]))

            if ollama_running:
                # Ollama is active → Update status
                self.set_ollama_label("Online")
                output_terminal("Info #21: Ollama is Online!", "green")
            else:
                # Ollama is not active → Update status
                self.set_ollama_label("Offline")
                output_terminal("Warning #7: Ollama is Offline!", "bg_yellow")

            # Aktualisiere UI-Elemente nur, wenn kein Test generiert wird
            if not self.is_generating_tests:
                self.update_generate_button_state(ollama_running)

            # Repeat the check
            self.after(5000, self.check_ollama_status)
            output_terminal("Info #22: Checking Ollama status..", "green")

        except Exception as e:
            # Error handling if `psutil.process_iter()` fails
            output_terminal(f"Error: Could not check Ollama status - {e}", "red")

    def update_generate_button_state(self, ollama_running):
        ''' Updates the generate button and status labels based on Ollama's status. '''
        if ollama_running:
            # Activate button only if no generation is running
            self.generate_label.configure(text="Ready", text_color="green")
            self.status_label.configure(text="OK", text_color="green")
            self.btn_generate.configure(state="normal", text=self.on_model_select(self.selected_model))
        else:
            # Deactivate button if no generation is running
            self.generate_label.configure(text="Not Ready", text_color="red")
            self.status_label.configure(text="-", text_color="red")
            self.btn_generate.configure(state="disabled", text="Ollama Offline - Cannot Generate")
