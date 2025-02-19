# main.py

"""
Search for all .py-files in a directory and generate Unit-Tests with a chosen prompt.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import ollama
import os
import subprocess


# global variables
folder_path = None
selected_model = None

def chose_folder():
    """
    Function for selecting the folder containing all .py files.
    """
    global folder_path

    folder_path = filedialog.askdirectory(title="Choose a Folder with Python Files")
    if folder_path:
        tb_chosen_folder.config(state="normal")
        tb_chosen_folder.delete("1.0", tk.END)
        tb_chosen_folder.insert("1.0", folder_path)
        tb_chosen_folder.config(state="disabled")

def chose_prompt_file():
    """
    Function for selecting the prompt file content.
    """
    prompt_file_path = filedialog.askopenfilename(
        title="Choose Your Prompt file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if prompt_file_path:
        with open(prompt_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            tb_chosen_prompt_file.config(state="normal")
            tb_chosen_prompt_file.delete("1.0", tk.END)
            tb_chosen_prompt_file.insert("1.0", file_content)
            tb_chosen_prompt_file.config(state="disabled")

def fetch_models():
    """
    Fetch available models by running the `ollama list` command in the terminal.
    """
    try:
        # executes `ollama list` in terminal
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        
        # loop through output lines and extract only the model name (first column)
        model_names = [line.split()[0] for line in result.stdout.splitlines() if not line.startswith("NAME")]
        
        print(model_names)
        return model_names
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Abrufen der Modelle mit 'ollama list': {e}")
        return []

def on_model_select(event):
    """
    Update the generate button text based on selected model.
    """
    global selected_model
    selected_model = combo_models.get()
    if selected_model:
        btn_generate.config(text=f"Generate Unit Test with '{selected_model}'")
    else:
        btn_generate.config(text="Generate")

def generate_tests():
    """
    Trigger the test generation process using the selected model.
    """
    if not selected_model:
        print("Please select an AI model.")
        return

    generate_tests_for_folder(selected_model)

def generate_tests_for_folder(model_name):
    """
    Generates unit tests for all .py files in the selected folder using the specified AI model.
    """
    global folder_path
    if not folder_path:
        print("No folder selected.")
        return

    prompt_text = tb_chosen_prompt_file.get("1.0", tk.END).strip()

    # create Tests-folder in the root of the selected folder
    tests_folder = os.path.join(folder_path, "Tests")
    os.makedirs(tests_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                code_text = file.read()

            full_prompt = f"{prompt_text}\n\n{code_text}\n"

            print(f"Generating test for {filename}...") # print progress in console

            # stream response from model
            stream = ollama.chat(
                model=model_name,
                messages=[{'role': 'user', 'content': full_prompt}],
                stream=True,
            )

            generated_output = ""
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    generated_output += content

            # extract Python code from generated output
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

            # save extracted Python code in the Tests folder
            test_filename = os.path.join(tests_folder, f"unit_test_{os.path.splitext(filename)[0]}_{model_name}.py")
            with open(test_filename, "w", encoding="utf-8") as test_file:
                test_file.write("\n".join(python_code_lines))
            print(f"Test for {filename} saved as {test_filename}.")
    print("\nAll tests successfully generated.")

# GUI setup
root = tk.Tk()
root.minsize(580, 500)
root.maxsize(580, 500)
root.title("AI Unit Test")
root.protocol("WM_DELETE_WINDOW", root.destroy)

main_frame = tk.Frame(root)
main_frame.pack(side="top", padx=10, pady=10, fill="x")

frame_one = tk.Frame(main_frame)
frame_one.pack(side="top", padx=10, pady=10, fill="x")

frame_two = tk.Frame(main_frame)
frame_two.pack(side="top", padx=10, pady=10, fill="x")

frame_three = tk.Frame(main_frame)
frame_three.pack(side="top", padx=10, pady=10, fill="x")

frame_four = tk.Frame(main_frame)
frame_four.pack(side="top", padx=10, pady=10, fill="x")

# frame one - selected folder
lbl_chosen_folder = tk.Label(frame_one, text="Selected Folder:", fg="white", font=("Arial", 12))
lbl_chosen_folder.pack(pady=5, anchor="w")

tb_chosen_folder = tk.Text(frame_one, height=1.5, width=40, wrap="word")
tb_chosen_folder.pack(side="left")
tb_chosen_folder.config(state="disabled")

btn_folder = tk.Button(frame_one, text="Choose Folder with Python Files", command=chose_folder)
btn_folder.pack(side="left", padx=5)

# frame two - selected prompt
lbl_chosen_prompt_file = tk.Label(frame_two, text="Prompt File:", fg="white", font=("Arial", 12))
lbl_chosen_prompt_file.pack(pady=5, anchor="w")

tb_chosen_prompt_file = tk.Text(frame_two, height=5, width=40, wrap="word")
tb_chosen_prompt_file.pack(side="left")
tb_chosen_prompt_file.config(state="disabled")

btn_prompt_file = tk.Button(frame_two, text="Choose Your Prompt File", command=chose_prompt_file)
btn_prompt_file.pack(side="left", padx=5)

# frame three - model selection dropdown
lbl_model_select = tk.Label(frame_three, text="Select AI Model:", fg="white", font=("Arial", 12))
lbl_model_select.pack(pady=5, anchor="w")

combo_models = ttk.Combobox(frame_three, state="readonly", width=40)
combo_models['values'] = fetch_models()  # Populate models from API
combo_models.pack(side="left")
combo_models.bind("<<ComboboxSelected>>", on_model_select)

# frame four - generate button
btn_generate = tk.Button(frame_four, text="Generate", command=generate_tests)
btn_generate.pack(side="top", pady=5, fill="x")

root.mainloop()