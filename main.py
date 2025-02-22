# Import Libraries
import customtkinter as ctk # GUI framework
import concurrent.futures # For parallel processing of test generation
import subprocess # Run system commands (fetch AI models from terminal)
import threading # For running test generation in a separate thread
import ollama # Communicate with the AI model
import psutil # Check if Ollama is running
import os # File and folder operations
from tkinter import filedialog # Open file/folder selection dialogs
from datetime import datetime # For timestamps in logs


# Global variables
# UI element Label
ollama_status_label = None
status_label = None
generate_label = None

# UI element Button
btn_generate = None
btn_exclude_folder = None
btn_folder = None
btn_prompt_file = None

# UI element Textbox
tb_chosen_folder = None
tb_chosen_prompt_file = None
tb_excluded_folder = None

# UI element Checkbox
checkbox_save_raw = None
checkbox_create_log = None

# UI element Others
root = None
combo_models = None
progress_bar = None

folder_path = None # Tracks main folder
prompt_file_path = None # Tracks prompt file
generation_thread = None # Tracks generation thread
model_names_cache = [] # Use cache (if available) to fetch models faster
is_generating_tests = False # Checks test generation
selected_model = None # Tracks model
excluded_folder_path = None # Tracks excluded folder


# Helper Functions
def output_terminal(msg, color):
    '''
    Prints a color-coded message on the terminal for debugging purposes.

    Process:
    - Assigns predefined colors to ANSI escape codes.
    - Formats the message with the selected color.
    - Resets the color after the message so as not to affect further terminal output.

    Args:
    - msg (str): The message to be displayed in the terminal.
    - color (str): The color name ('red', 'green', 'yellow', 'blue', 'reset').
    '''
    all_colors = {
        "red": "\033[31m",          # red text
        "green": "\033[32m",        # green text
        "yellow": "\033[33m",       # yellow text
        "blue": "\033[34m",         # blue text
        "bg_red": "\033[41m",       # red background
        "bg_yellow": "\033[43m",    # yellow background
        "reset": "\033[0m"          # Reset to standard
    }

    color_code = all_colors.get(color, all_colors["reset"]) # Standard color as Fallback
    print(f"{color_code}{msg}{all_colors['reset']}") # Resets color at the end

def set_status_label(msg):
    '''
    Updates the status label in the UI with a new message.

    Parameters:
    - msg (str): The new text that will be displayed in the status label.

    This method:
    - Sets the text of the 'status_label' widget to the passed value
    - Uses the color green for the text by default
    '''
    global status_label
    status_label.configure(text=msg, text_color="green")

def set_generate_label(msg):
    '''
    Updates the label for the test generation status in the UI.

    Parameters:
    - msg (str): The new message describing the current test generation status.

    This method:
    - Sets the text of the 'generate_label' widget to the passed value
    - Uses the color green for the text by default
    '''
    global generate_label
    generate_label.configure(text=msg, text_color="green")

def set_ollama_label(opt):
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
    global ollama_status_label
    if opt == "Online":
        ollama_status_label.configure(text="Ollama Online", text_color="green")
    elif opt == "Offline":
        ollama_status_label.configure(text="Ollama Offline", text_color="red")
    else:
        ollama_status_label.configure(text="Error", text_color="grey")
        return


# Functions - Generating Test
def generate_tests():
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
    global selected_model, generation_thread, excluded_folder_path, folder_path, root, btn_generate, is_generating_tests, generate_label, prompt_file_path, checkbox_save_raw, checkbox_create_log, btn_folder, btn_exclude_folder, btn_prompt_file

    # Check if main folder is selected
    if not folder_path:
        output_terminal("Error #1-Please choose a folder.", "bg_red")
        set_status_label("Please select a folder.")
        return
    
    # Check if a prompt exists
    if not tb_chosen_prompt_file.get("1.0", ctk.END).strip():
        output_terminal("Error #2-No prompt selected.", "bg_red")
        set_status_label("Please choose a prompt.")
        return
    
    # Check if an AI model has been selected
    if selected_model == "None":
        output_terminal("Error #3-Please select an AI model before generating tests.", "bg_red")
        set_status_label("Please choose an AI model.")
        return
    
    output_terminal(f"Info #1-Mardown-Checkbox Status is: {checkbox_save_raw.get()}", "green")
    output_terminal(f"Info #2-Log-Checkbox Status is: {checkbox_create_log.get()}", "green")

    # Search for Python files in the selected folder
    py_files = get_python_files(folder_path, excluded_folder_path)

    # If no Python files were found, end the generation
    if not py_files:
        output_terminal("Warning #1-No Python files found in the selected folder.", "bg_yellow")
        set_status_label("No Python files found.")
        return

    # Display the number of files found
    total_files = len(py_files)
    output_terminal(f"Info #3-Found {total_files} Python file(s): {', '.join(os.path.basename(f) for f in py_files)}", "green")
    
    # Update status for current generation
    set_generate_label("Generation in progress...")
    set_status_label(f"Total files found: {total_files}")

    # Initialize the progress bar
    initialize_progress_bar(total_files)

    # Start the generation
    is_generating_tests = True # Set variable that the generation is running
    btn_generate.configure(state="disabled", text="Generating, please wait...")
    btn_exclude_folder.configure(state="disabled")
    btn_folder.configure(state="disabled")
    btn_prompt_file.configure(state="disabled")
    combo_models.configure(state="disabled")
    checkbox_save_raw.configure(state="disabled")
    checkbox_create_log.configure(state="disabled")

    # Start the generation in a separate thread to avoid blocking the GUI
    generation_thread = threading.Thread(target=generate_tests_for_folder, args=(selected_model, total_files, py_files), daemon=True)
    generation_thread.start()
    
    # Track the progress of the generation
    check_generation_completion()

def generate_tests_for_folder(model_name, total_files, py_files):
    '''
    Generates unit tests for Python files in the selected folder.

    This method:
    - Reads a custom prompt from the GUI.
    - Uses an AI model to generate unit tests for each Python file.
    - Saves the generated tests and logs the process.
    - Updates progress bars and UI elements accordingly.

    Args:
    - model_name (str): Selected AI model.
    - total_files (int): Total number of Python files.
    - py_files (list): List of Python files to be processed.
    '''
    global folder_path

    # Create the 'Tests' folder
    prompt_text = tb_chosen_prompt_file.get("1.0", ctk.END).strip()
    tests_folder = os.path.join(folder_path, "Tests")
    os.makedirs(tests_folder, exist_ok=True)

    if not py_files:
        output_terminal("Warning #2-No Python files found in the selected folder.", "bg_yellow")
        return

    # If log storage is activated
    log_file_path = os.path.join(tests_folder, f"utg-{model_name}.log") if checkbox_create_log.get() else None
    log_file = open(log_file_path, "a", encoding="utf-8") if log_file_path else None

    # If Log is active, start it
    if log_file:
        start_time = datetime.now()
        log_file.write(f"\n--- Test Generation Started ---\n")
        log_file.write(f"Model: {model_name}\n")
        log_file.write(f"Date: {start_time.strftime('%Y-%m-%d')}\n")
        log_file.write(f"Start Time: {start_time.strftime('%H:%M:%S')}\n")
        log_file.write(f"Folder: {folder_path}\n\n")

    # Parallelization of the test generation
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(generate_test_for_file, model_name, prompt_text, file, tests_folder): file
            for file in py_files
        }
        completed = 0

        for future in concurrent.futures.as_completed(futures):
            filename = futures[future]
            try:
                test_code, generated_output, code_text = future.result()

                if test_code is None:
                    output_terminal(f"Error #4: Failed to generate test for {filename}", "bg_red")
                    continue

                # Save test file
                test_filename = save_files(filename, model_name, tests_folder, prompt_text, code_text, generated_output)

                with open(test_filename, "w", encoding="utf-8") as test_file:
                    test_file.write(test_code)

                # If Log is active, write the entry
                if log_file:
                    log_file.write(f"✔ Completed: {filename} at {datetime.now().strftime('%H:%M:%S')}\n")

                completed += 1
                output_terminal(f"Info #4: Test generated for {filename} ({completed}/{total_files})", "green")
                set_status_label(f"Generated Tests for ({completed}/{total_files}).")
                
                update_progress_bar(completed, total_files)

            except Exception as e:
                output_terminal(f"Error #5: Failed to generate test for {filename}: {e}", "bg_red")
                if log_file:
                    log_file.write(f"ERROR: generating test for {filename} - {e}\n")

    # If log is active, close it
    if log_file:
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        log_file.write(f"\n--- Test Generation Completed ---\n")
        log_file.write(f"End Time: {end_time.strftime('%H:%M:%S')}\n")
        log_file.write(f"Elapsed Time: {str(elapsed_time)}\n\n")
        log_file.close()
        output_terminal(f"Info #5: Log file saved: {log_file_path}", "green")

def generate_test_for_file(model_name, prompt_text, filename, tests_folder):
    '''
    Generates a unit test for a single Python file using the AI model.

    This method:
    - Reads the contents of the specified Python file.
    - Prepares an AI model prompt including the code.
    - Extracts the generated test code from the AI response.

    Args:
    - model_name (str): The AI model used.
    - prompt_text (str): User-defined prompt.
    - filename (str): The Python file to be processed.

    Return:
    - Tuple (str, str, str): Generated test code, raw AI response, original code.
    '''
    try:
        # Read in file content
        with open(filename, 'r', encoding='utf-8') as file:
            code_text = file.read()

        # Prepare prompt and code for the model
        full_prompt = f"{prompt_text}\n\n{code_text}\n"
        output_terminal(f"Info #6: Generating test for {filename}...", "green")

        # Streamed output retrieved from the AI model
        stream = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True,
        )

        generated_output = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                generated_output += chunk['message']['content']

        # Extract Python code from the AI response
        python_code_lines = []
        in_code_block = False

        for line in generated_output.splitlines():
            if line.strip() == "```python":
                in_code_block = True
                continue
            elif line.strip() == "```" and in_code_block:
                in_code_block = False
                continue
            if in_code_block:
                python_code_lines.append(line)

        # Return generated test code
        return "\n".join(python_code_lines), generated_output, code_text

    except Exception as e:
        output_terminal(f"Error #6: Failed to generate test for {filename}: {e}", "bg_red")
        return None, None, None # Error

def get_python_files(folder_path, excluded_folder_path):
    '''
    Monitors the test generation process and resets the user interface after completion.

    This method:
    - Checks whether the generation thread is still running.
    - If completed:
        - Updates the user interface labels.
        - Resets the progress bar.
        - Activates the UI elements again.
    '''
    py_files = []
    for dirpath, _, files in os.walk(folder_path):
        output_terminal(f"Info #7: Checking folder: {dirpath}", "green")

        # Skip excluded folders
        if excluded_folder_path and os.path.commonpath([excluded_folder_path, dirpath]) == excluded_folder_path:
            output_terminal(f"Info #8-Skipping excluded folder: {dirpath}", "red")
            continue

        # Add all .py files to the list
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(dirpath, file)
                output_terminal(f"Info #9-Found Python file: {file_path}", "yellow")
                py_files.append(file_path)

    # If no files were found, output debugging message
    if not py_files:
        output_terminal("Error #7-No Python files found!", "bg_red")

    return py_files

def initialize_progress_bar(total_files):
    '''
    Initializes the progress bar for the test generation process.

    Parameters:
    - total_files (int): The total number of files to be processed.

    This method:
    - Sets the progress bar ('progress_bar') to 0.0 (initial state)
    - Outputs an info message in the terminal to confirm the initializatio
    '''
    global progress_bar

    # Reset progress bar
    progress_bar.set(0.0)

    output_terminal(f"Info #10: Progress bar initialized for {total_files} files.", "green")

def check_generation_completion():
    '''
    Monitors the test generation process and resets UI elements after completion.

    This method:
    - Checks every second if the test generation thread is still running.
    - After completion:
        - Updates the UI labels.
        - Resets the progress bar.
        - Re-enables the UI buttons and input fields.
        - Ensures a smooth transition for a new test generation session.
    '''
    global generation_thread, root, is_generating_tests

    # If the thread is still running, check again after 1 second
    if generation_thread and generation_thread.is_alive():
        root.after(1000, check_generation_completion)
    else:
        # Generation completed
        output_terminal("Info #11-SUCCESS: Done generating all tests!", "blue")
        set_generate_label("Done generating tests.")

        # Reset status so that a new generation can be started
        is_generating_tests = False

        # Activate button again
        root.after(4000, lambda: btn_generate.configure(state="normal", text=on_model_select(selected_model)))

        # Reset states
        btn_exclude_folder.configure(state="normal")
        btn_folder.configure(state="normal")
        btn_prompt_file.configure(state="normal")
        combo_models.configure(state="normal")
        checkbox_save_raw.configure(state="normal")
        checkbox_create_log.configure(state="normal")

        # Reset Labels after 4 seconds
        root.after(4000, lambda: reset_progress_bar())
        root.after(4000, lambda: set_generate_label("Ready"))
        root.after(4000, lambda: set_status_label("OK"))

def reset_progress_bar():
    '''
    Resets the progress bar to the initial state.

    This method:
    - Sets the value of the progress bar ('progress_bar') to 0.0
    - Outputs an info message in the terminal to confirm the reset
    '''
    global progress_bar

    # Reset progress bar
    progress_bar.set(0.0)

    output_terminal(f"Info #12: Progress bar reset.", "green")

def save_files(filename, model_name, tests_folder, prompt_text, code_text, generated_output):
    '''
    Saves the generated test file and optionally a Markdown documentation.

    This method:
    - Generates a suitable file name for the unit test.
    - Writes the test code to a '.py' file.
    - If saving in Markdown is enabled, a '.md' file with test details is created.

    Args:
    - filename (str): The original Python filename.
    - model_name (str): The AI model used for the generation.
    - tests_folder (str): Directory where the test files are stored.
    - prompt_text (str): The prompt text used for test generation.
    - code_text (str): Content of the original Python code.
    - generated_output (str): Unprocessed response generated by the AI.

    Return:
    - str: Path to the saved '.py' test file.
    '''
    global checkbox_save_raw, checkbox_create_log

    # Generated test file name
    base_filename = os.path.basename(os.path.splitext(filename)[0])
    test_filename = os.path.join(tests_folder, f"unit_test_{base_filename}_{model_name}.py")

    # If Markdown saving is activated
    if checkbox_save_raw.get():
        md_filename = os.path.join(tests_folder, f"unit_test_{base_filename}_{model_name}.md")
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write("# Unit Test Documentation\n")
            md_file.write(f"## Original File: {filename}\n\n")
            md_file.write(f"### Model: {model_name}\n\n")
            md_file.write(f"### Prompt\n\n```\n{prompt_text}\n\n{code_text}\n```\n\n")
            md_file.write(f"### Generated Output\n\n```\n{generated_output}\n```\n")
        output_terminal(f"Info #13: Markdown saved: {md_filename}", "blue")

    return test_filename# Returns the test file path

def update_progress_bar(completed_tests, total_files):
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
    global progress_bar

    if total_files == 0: # Prevent division by zero
        output_terminal(f"Warning #3: No files to process, progress bar update skipped.", "bg_yellow")
        return

    progress_value = completed_tests / total_files # Value between 0.0 and 1.0
    progress_bar.set(progress_value)

    output_terminal(f"Info #14: Progress: {completed_tests}/{total_files} tests completed ({progress_value*100:.2f}%)", "yellow")

def check_ollama_status():
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
    global ollama_status_label, btn_generate, generate_label, root, is_generating_tests

    # Check whether all GUI elements are present
    if not all([ollama_status_label, btn_generate, generate_label]):
        output_terminal(f"Error #8: Some GUI elements are None! The interface might not be fully initialized.", "bg_red")
        return # If GUI is not ready, cancel

    try:
        # Check whether a process with “ollama” in its name is running
        ollama_running = any("ollama" in proc.info["name"].lower() for proc in psutil.process_iter(["name"]))

        if ollama_running:
            # Ollama is active → Update status
            set_ollama_label("Online")
            if not is_generating_tests:
                output_terminal("Info #15: Ollama is Online!", "green")

            # Activate button only if no generation is running
            if not is_generating_tests:
                btn_generate.configure(state="normal", text=on_model_select(selected_model))
        else:
            # Ollama is not active → Update status
            set_ollama_label("Offline")
            output_terminal("Warning #4: Ollama is Offline!", "bg_yellow")

            # Deactivate button if no generation is running
            if not is_generating_tests:
                btn_generate.configure(state="disabled", text="Ollama Offline - Cannot Generate")

        # Repeat the check after 5 seconds
        root.after(5000, check_ollama_status)
        output_terminal("Info #16: Checking Ollama status..", "green")

    except Exception as e:
        # Error handling if `psutil.process_iter()` fails
        output_terminal(f"Error #9: Could not check Ollama status - {e}", "bg_red")


# Function - Select Folder and Files
def choose_folder():
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
    global folder_path, tb_chosen_folder, tb_chosen_prompt_file, btn_exclude_folder, status_label

    # If no folder was selected, cancel
    folder_path = filedialog.askdirectory(title="Choose a Folder with Python Files")

    # ❌ Falls kein Ordner gewählt wurde, breche ab
    if not folder_path:
        output_terminal("Warning #5: No folder selected.", "bg_yellow")
        return
    
    # Show the selected folder in the UI text field
    tb_chosen_folder.configure(state="normal")
    tb_chosen_folder.delete("1.0", ctk.END)
    tb_chosen_folder.insert("1.0", folder_path)
    tb_chosen_folder.configure(state="disabled")

    # Activate the button to exclude subfolders
    btn_exclude_folder.configure(state="normal")

    # Search for a prompt file (`prompt.txt`, `prompt.md`, `prompt.doc`) in the selected folder
    prompt_file_path = None
    for ext in ["txt", "md", "doc"]: # File format list
        potential_path = os.path.join(folder_path, f"prompt.{ext}")
        if os.path.exists(potential_path):
            prompt_file_path = potential_path
            break # Erste gefundene Datei verwenden

    # If a prompt file was found, load it into the prompt text field
    if prompt_file_path:
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as file:
                file_content = file.read().strip() # Remove space at the beginning/end

            # Ensure that `self.tb_chosen_prompt_file` exists
            tb_chosen_prompt_file.configure(state="normal")
            tb_chosen_prompt_file.delete("1.0", ctk.END)
            tb_chosen_prompt_file.insert("1.0", file_content)
        
            # Success message in the terminal
            output_terminal("Info #17: Automatically found prompt file: '{os.path.basename(prompt_file_path)}'", "blue")
        
        except Exception as e:
            # Error handling if the file cannot be read
            output_terminal(f"Error #10: Could not read prompt file - {e}", "bg_red")
    
    else:
        # If no prompt file was found
        output_terminal("Warning #6: No prompt file found in the selected folder.", "bg_yellow")

    # Confirm successful selection in the terminal and GUI
    output_terminal(f"Info #18: Your selected folder: '{folder_path}'", "green")

def choose_exclude_folder():
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
    global excluded_folder_path, tb_excluded_folder

    # Check whether a main folder has been selected
    if not folder_path:
        output_terminal(f"Error #11: No main folder selected. Please choose a main folder first.", "bg_red")
        return
    
    # If an exclusion folder already exists, open the dialog there - otherwise in the main folder
    start_path = excluded_folder_path if excluded_folder_path else folder_path

    # Open the file dialog for the folder selection
    excluded_folder_path = filedialog.askdirectory(title="Choose a Subfolder to Exclude", initialdir=start_path)

    # If the user cancels the selection, empty the text field and display a message
    if not excluded_folder_path:
        output_terminal("Info #19: Folder exclusion was cancelled.", "yellow")
        tb_excluded_folder.configure(state="normal") # Unlock text box so that we can change the text
        tb_excluded_folder.delete("1.0", ctk.END) # Delete text box content
        tb_excluded_folder.configure(state="disabled") # Deactivate text box again
        return # Exit function so that no error message appears
    
    # Check whether the selected folder is within the main folder
    try:
        rel_path = os.path.relpath(excluded_folder_path, folder_path)
        if rel_path.startswith(".."):
            raise ValueError("Selected folder is not a subfolder!")

        # Valid subfolder -> Update text field
        tb_excluded_folder.configure(state="normal")
        tb_excluded_folder.delete("1.0", ctk.END)
        tb_excluded_folder.insert("1.0", excluded_folder_path)
        tb_excluded_folder.configure(state="disabled")
        output_terminal(f"Info #20: Excluded folder: '{excluded_folder_path}'", "green")

    except ValueError:
        # Error message if the folder is not within the main folder
        output_terminal("Error #12: The excluded folder must be a subfolder of the main folder.", "bg_red")
        excluded_folder_path = None

def choose_prompt_file():
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
    global prompt_file_path

    try:
        # Open file dialog to select a prompt file
        prompt_file_path = filedialog.askopenfilename(
            title="Choose Your Prompt File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        # If no file was selected, cancel
        if not prompt_file_path:
            output_terminal("Warning #7: No prompt file selected.", "bg_yellow")
            return

        # Open file and read content
        with open(prompt_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read().strip()

        # Update text field (first unlock, then lock)
        tb_chosen_prompt_file.configure(state="normal")
        tb_chosen_prompt_file.delete("1.0", ctk.END)
        tb_chosen_prompt_file.insert("1.0", file_content)
        tb_chosen_prompt_file.configure(state="disabled")

        output_terminal(f"Info #21: Prompt manually loaded from '{os.path.basename(prompt_file_path)}'", "green")

    except Exception as e:
        # Error handling if file cannot be opened
        output_terminal(f"Error #13: Could not load prompt file - {e}", "bg_red")

def fetch_models():
    '''
    Prints a color-coded message on the terminal for debugging purposes.

    This method:
    - Assigns predefined colors to ANSI escape codes.
    - Formats the message with the selected color.
    - Resets the color after the message so as not to affect further terminal output.

    Args:
    - msg (str): The message to be displayed in the terminal.
    - color (str): The color name ('red', 'green”, 'yellow', 'blue', 'reset').
    '''
    global model_names_cache

    # If models are already stored in the cache, use them directly (performance optimization)
    if model_names_cache: # Prevents the cache from being overwritten again and again
        output_terminal("Info #22: Using cached model list.", "green")
        return model_names_cache
    
    try:
        # Execute the command `ollama list` to load models from the terminal
        output_terminal("Info #23: Fetching available AI models...", "green")

        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)

        # Process the terminal output: Extract only the model names (first column of the output)
        model_names = [line.split()[0] for line in result.stdout.splitlines() if not line.startswith("NAME")]

        # Save the models in the cache to avoid repeated queries
        model_names_cache = model_names

        output_terminal(f"Info #24: Available AI models: {', '.join(model_names)}", "green")

        return model_names

    except subprocess.CalledProcessError as e:
        # Error handling if `ollama list` fails
        output_terminal(f"Error #8: Failed to fetch models using 'ollama list': {e}", "bg_red")
        return [] # Fallback: Return of an empty list

def on_model_select(event):
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
    global selected_model

    # Update `selected_model` with the new value or set “None” as default
    selected_model = event if event else "None"

    # Set the value of the ComboBox explicitly (prevents errors in the event of unexpected events)
    combo_models.set(selected_model)

    # If “None” was selected, reset the button to the default text
    if selected_model == "None":
        btn_generate.configure(text="Generate")
        output_terminal("Info #25: No model selected. Please choose an AI model.", "yellow")
        return "Generate"

     # Update the button text with the selected model
    new_text = f"Generate Unit Test with '{selected_model}'"
    btn_generate.configure(text=new_text)
    
    output_terminal(f"Info #26: Model selected: '{selected_model}'", "green")

    return new_text


# GUI
def setup_gui():
    '''
    A GUI application for the automated generation of unit tests using AI.

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
    global root, ollama_status_label, btn_generate, status_label
    global tb_chosen_folder, tb_chosen_prompt_file, btn_exclude_folder, tb_excluded_folder
    global generate_label, combo_models, progress_bar, checkbox_save_raw, checkbox_create_log
    global btn_folder, btn_prompt_file

    # Sets design mode and color scheme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Main window settings
    root = ctk.CTk()
    root.geometry("600x710")
    root.minsize(600, 710)
    root.maxsize(600, 710)
    root.title("Unit Test-Generation with AI [GenUnit]")
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Main frame for UI elements
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Status frame
    frame_label = ctk.CTkFrame(main_frame)
    frame_label.pack(padx=10, pady=10, fill="x")
    frame_label.columnconfigure((0, 1, 2), weight=1)

    # Status labels
    generate_label = ctk.CTkLabel(frame_label, text="Ready", text_color="green", font=("Arial", 14))
    generate_label.grid(row=0, column=0, sticky="w", padx=4)

    status_label = ctk.CTkLabel(frame_label, text="OK", text_color="green", font=("Arial", 14))
    status_label.grid(row=0, column=1, sticky="n", padx=4)

    ollama_status_label = ctk.CTkLabel(frame_label, text="Checking...", text_color="orange", font=("Arial", 14))
    ollama_status_label.grid(row=0, column=2, sticky="e", padx=4)

    # Folder selection
    frame_select_folder = ctk.CTkFrame(main_frame)
    frame_select_folder.pack(padx=10, pady=10, fill="x")

    lbl_chosen_folder = ctk.CTkLabel(frame_select_folder, text="Selected Folder:", font=("Arial", 14))
    lbl_chosen_folder.pack(pady=4, anchor="w", padx=4)

    tb_chosen_folder = ctk.CTkTextbox(frame_select_folder, height=30, state="disabled")
    tb_chosen_folder.pack(side="left", padx=4, pady=4, expand=True, fill="x")

    btn_folder = ctk.CTkButton(frame_select_folder, text="Choose Folder", command=choose_folder)
    btn_folder.pack(side="left", padx=5, pady=4)

    # Exclude a subfolder
    frame_exclude_folder = ctk.CTkFrame(main_frame)
    frame_exclude_folder.pack(padx=10, pady=10, fill="x")

    lbl_excluded_folder = ctk.CTkLabel(frame_exclude_folder, text="Excluded Folder:", font=("Arial", 14))
    lbl_excluded_folder.pack(pady=4, anchor="w", padx=4)

    tb_excluded_folder = ctk.CTkTextbox(frame_exclude_folder, height=30, state="disabled")
    tb_excluded_folder.pack(side="left", padx=4, pady=4, expand=True, fill="x")

    btn_exclude_folder = ctk.CTkButton(frame_exclude_folder, text="Choose Excluded Folder", command=choose_exclude_folder, state="disabled")
    btn_exclude_folder.pack(side="left", padx=5, pady=4)

    # Select prompt file
    frame_prompt = ctk.CTkFrame(main_frame)
    frame_prompt.pack(padx=10, pady=10, fill="x")

    lbl_chosen_prompt_file = ctk.CTkLabel(frame_prompt, text="Prompt File:", font=("Arial", 14))
    lbl_chosen_prompt_file.pack(pady=4, anchor="w", padx=4)

    tb_chosen_prompt_file = ctk.CTkTextbox(frame_prompt, height=100)
    tb_chosen_prompt_file.pack(side="left", padx=4, pady=4, expand=True, fill="x")

    btn_prompt_file = ctk.CTkButton(frame_prompt, text="Choose Prompt File", command=choose_prompt_file)
    btn_prompt_file.pack(side="left", padx=5, pady=4)

    # AI model selection
    frame_model_selection = ctk.CTkFrame(main_frame)
    frame_model_selection.pack(padx=10, pady=10, fill="x")

    lbl_model_select = ctk.CTkLabel(frame_model_selection, text=" Select AI Model:", font=("Arial", 14))
    lbl_model_select.grid(row=0, column=0, padx=(0, 10), pady=4, sticky="w")

    model_list = fetch_models()

    combo_models = ctk.CTkComboBox(frame_model_selection, values=model_list, command=on_model_select, width=300)
    combo_models.grid(row=0, column=1, padx=0, pady=4, sticky="w")
    combo_models.set("None")

    # Additional options
    frame_generate = ctk.CTkFrame(main_frame)
    frame_generate.pack(padx=10, pady=10, fill="x")

    checkbox_save_raw = ctk.CTkCheckBox(frame_generate, text="Save Raw Markdown")
    checkbox_save_raw.pack(side="top", pady=4)
    checkbox_save_raw.select() # Activated by default

    checkbox_create_log = ctk.CTkCheckBox(frame_generate, text="Create Log-File")
    checkbox_create_log.pack(side="top", pady=4)
    checkbox_create_log.select() # Activated by default

    # Start test generation
    btn_generate = ctk.CTkButton(frame_generate, text="Generate", command=generate_tests)
    btn_generate.pack(side="top", pady=4)

    # Progress bar
    frame_progress = ctk.CTkFrame(main_frame)
    frame_progress.pack(padx=10, pady=10, fill="x")

    progress_bar = ctk.CTkProgressBar(frame_progress, orientation="horizontal", width=400, mode="determinate")
    progress_bar.pack(pady=10, anchor="center")
    progress_bar.set(0.0)

    # Footer with trademark & disclaimer
    trademark_label = ctk.CTkLabel(main_frame, text="© 2025 Created by Berkant - GenUnit", font=("Arial", 10))
    trademark_label.pack(pady=5, anchor="center")

    disclaimer_label = ctk.CTkLabel(main_frame, text="Use at your own risk.", font=("Arial", 10), text_color="red")
    disclaimer_label.pack(pady=5, anchor="center")

    check_ollama_status()
    root.mainloop()

setup_gui()