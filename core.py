import customtkinter as ctk # GUI framework (needed for accessing UI elements)
import concurrent.futures # For parallel processing of test generation
import ollama # Communicate with the AI model
import os # File handling and folder operations
from helpers import output_terminal # Print colored messages to the terminal
from datetime import datetime # For timestamps in logs

class TestGenerator:
    '''
    Handles the automatic generation of unit tests for Python files.

    Responsibilities:
    - Extracts Python files from the selected folder.
    - Uses an AI model to generate unit tests.
    - Saves the tests in the appropriate format (Python/Markdown).
    - Takes care of updating the user interface (progress bar, logging and status messages).
    '''
    def __init__(self, gui):
        '''
        Initializes the TestGenerator class.

        Args:
        - gui (GenUnitApp): The instance of the GUI application to interact with the UI components.
        '''
        super().__init__()
        self.gui = gui

        self.error = False

    # Test generation
    def generate_tests_for_folder(self, model_name, total_files, py_files):
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
        # Create the 'Tests' folder
        prompt_text = self.gui.tb_chosen_prompt_file.get("1.0", ctk.END).strip()
        tests_folder = os.path.join(self.gui.folder_path, "Tests")
        os.makedirs(tests_folder, exist_ok=True)

        if not py_files:
            output_terminal("Warning #2-No Python files found in the selected folder.", "bg_yellow")
            return

        # If log storage is activated
        formatted_model_name = self.format_model_name(model_name)
        log_file_path = os.path.join(tests_folder, f"unit_test_log_file-{formatted_model_name}.log") if self.gui.checkbox_create_log.get() else None
        log_file = open(log_file_path, "a", encoding="utf-8") if log_file_path else None

        # If Log is active, start it
        if log_file:
            start_time = datetime.now()
            log_file.write(f"\n--- Test Generation Started ---\n")
            log_file.write(f"Model: {model_name}\n")
            log_file.write(f"Date: {start_time.strftime('%Y-%m-%d')}\n")
            log_file.write(f"Start Time: {start_time.strftime('%H:%M:%S')}\n")
            log_file.write(f"Folder: {self.gui.folder_path}\n\n")

        # Parallelization of the test generation
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.generate_test_for_file, model_name, prompt_text, file): file
                for file in py_files
            }
            completed = 0

            for future in concurrent.futures.as_completed(futures):
                filename = futures[future]
                try:
                    test_code, generated_output, code_text = future.result()

                    if test_code is None:
                        output_terminal(f"Error #5: Failed to generate test for {filename}", "bg_red")
                        self.error = True
                        continue

                    # Save test file
                    test_filename = self.save_files(filename, model_name, tests_folder, prompt_text, code_text, generated_output)

                    with open(test_filename, "w", encoding="utf-8") as test_file:
                        test_file.write(test_code)

                    # If Log is active, write the entry
                    if log_file:
                        log_file.write(f"✔ Completed: {filename} at {datetime.now().strftime('%H:%M:%S')}\n")

                    completed += 1
                    output_terminal(f"Info #7: Test generated for {filename} ({completed}/{total_files})", "yellow")
                    self.gui.set_status_label(f"Generated Tests for ({completed}/{total_files}).")
                    
                    self.gui.update_progress_bar(completed, total_files)

                except Exception as e:
                    output_terminal(f"Error #6: Failed to generate test for {filename}: {e}", "bg_red")
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
            output_terminal(f"Info #51: Log file saved: {log_file_path}", "yellow")

    def generate_test_for_file(self, model_name, prompt_text, filename):
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
            output_terminal(f"Info #6: Generating test for {filename}...", "yellow")

            # Streamed output retrieved from the AI model
            try:
                stream = ollama.chat(
                    model=model_name,
                    messages=[{'role': 'user', 'content': full_prompt}],
                    stream=True,
                )
            except Exception as e:
                output_terminal(f"Error #4: AI model failed to generate test for {filename}: {e}", "bg_red")
                return None, None, None

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
            output_terminal(f"Error #4: Failed to generate test for {filename}: {e}", "bg_red")
            self.error = True
            return None, None, None # Error

    # File management
    def get_python_files(self, folder_path, excluded_folder_path):
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
            output_terminal(f"Info #54: Checking folder: {dirpath}", "blue")

            # Skip excluded folders
            if excluded_folder_path and os.path.commonpath([excluded_folder_path, dirpath]) == excluded_folder_path:
                output_terminal(f"Info #56: Skipping excluded folder: {dirpath}", "red")
                continue

            # Add all .py files to the list
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(dirpath, file)
                    output_terminal(f"Info #50: Found Python file: {file_path}", "yellow")
                    py_files.append(file_path)

        # If no files were found, output debugging message
        if not py_files:
            self.gui.set_status_label("No Python files found.") #MARK:Check
            self.gui.is_generating_tests = False
            output_terminal("❌ No Python files found!", "red")
            return

        return py_files

    def save_files(self, filename, model_name, tests_folder, prompt_text, code_text, generated_output):
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
        # Generated test file name
        formatted_model_name = self.format_model_name(model_name)
        base_filename = os.path.basename(os.path.splitext(filename)[0])
        test_filename = os.path.join(tests_folder, f"unit_test_{base_filename}_{formatted_model_name}.py")

        # If Markdown saving is activated
        if self.gui.checkbox_save_raw.get():
            md_filename = os.path.join(tests_folder, f"unit_test_{base_filename}_{formatted_model_name}.md")
            content = "\n".join([
                "# Unit Test Documentation",
                f"## Original File: {filename}\n",
                f"### Model: {model_name}\n",
                f"### Prompt\n```\n{prompt_text}\n\n{code_text}\n```",
                f"### Generated Output\n```\n{generated_output}\n```"
            ])
            with open(md_filename, "w", encoding="utf-8") as md_file:
                md_file.write(content)
        output_terminal(f"Info #52: Markdown file saved: {test_filename}", color="yellow")
        return test_filename # Returns the test file path

    def format_model_name(self, model_name):
        '''
        Formats the model name by replacing invalid characters.

        Parameters:
        - model_name (str): The original name of the AI model.

        This method:
        - Replaces ":" with "_" to ensure compatibility with Windows file system.
        - Returns the formatted model name without restricted characters.
        '''
        formatted_model_name = model_name.replace(":", "_")
        return formatted_model_name


    # Threading & Progress
    def check_generation_completion(self):
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
        # If the thread is still running, check again after 1 second
        if getattr(self.gui, "generation_thread", None) and self.gui.generation_thread.is_alive():
            self.gui.after(1000, self.check_generation_completion)
        else:
            # Generation completed
            if self.error == True:
                output_terminal("Error #20: Error: Not all tests created!", "bg_red")
                self.gui.set_generate_label("Error while generating tests.", "red")
            else:
                output_terminal("Info #4-Success: Done generating all tests!", "blue")
                self.gui.set_generate_label("Done generating tests.")

            # Reset status so that a new generation can be started
            self.gui.is_generating_tests = False

            # Activate button again
            self.gui.after(4000, lambda: self.gui.btn_generate.configure(state="normal", text=self.gui.on_model_select(self.gui.selected_model)))

            # Reset states
            self.gui.btn_exclude_folder.configure(state="normal")
            self.gui.btn_folder.configure(state="normal")
            self.gui.btn_prompt_file.configure(state="normal")
            self.gui.combo_models.configure(state="normal")
            self.gui.checkbox_save_raw.configure(state="normal")
            self.gui.checkbox_create_log.configure(state="normal")

            # Reset Labels after 4 seconds
            self.gui.after(4000, lambda: self.gui.reset_progress_bar())
            self.gui.after(4000, lambda: self.gui.set_generate_label("Ready"))
            self.gui.after(4000, lambda: self.gui.set_status_label("OK"))
