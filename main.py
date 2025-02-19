# main.py

"""
Search for all .py-files in a directory and generate Unit-Tests with a chosen prompt.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import ollama
import os
import subprocess
import concurrent.futures # for parallel processing
import threading # for GUI responsiveness
import psutil # check Ollama-process
from datetime import datetime # get current date


# global variables
folder_path = None
selected_model = None
generation_thread = None # keep track of the generation thread


def chose_folder():
    global folder_path

    folder_path = filedialog.askdirectory(title="Choose a Folder with Python Files")
    if folder_path:
        tb_chosen_folder.config(state="normal")
        tb_chosen_folder.delete("1.0", tk.END)
        tb_chosen_folder.insert("1.0", folder_path)
        tb_chosen_folder.config(state="disabled")

        prompt_file_path = None
        for ext in ["txt", "md", "doc"]: # allowed extensions
            potential_path = os.path.join(folder_path, f"prompt.{ext}")
            if os.path.exists(potential_path):
                prompt_file_path = potential_path
                break

        if prompt_file_path:
            with open(prompt_file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                tb_chosen_prompt_file.config(state="normal")
                tb_chosen_prompt_file.delete("1.0", tk.END)
                tb_chosen_prompt_file.insert("1.0", file_content)
                tb_chosen_prompt_file.config(state="disabled")
            print(f"Automatically found prompt file: '{prompt_file_path}'")
        else:
            print("No prompt file found in the selected folder.")
    print(f"Your selected folder: '{folder_path}'")

def chose_prompt_file():
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
        print(f"Your chosen prompt: '{file_content}'")

def fetch_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        model_names = [line.split()[0] for line in result.stdout.splitlines() if not line.startswith("NAME")]
        print(f"All available models: {model_names}")
        return model_names
    except subprocess.CalledProcessError as e:
        print(f"Error fetching models with 'ollama list': {e}")
        return []

def on_model_select(event):
    global selected_model

    selected_model = combo_models.get()
    btn_generate.config(text=f"Generate Unit Test with '{selected_model}'" if selected_model else "Generate")
    print(f"Model selected: '{selected_model}'")

def generate_tests():
    global generation_thread

    if not selected_model:
        print("Please select an AI model.")
        return

    status_label.config(text="Generating, please wait...", fg="orange")

    generation_thread = threading.Thread(target=generate_tests_for_folder, args=(selected_model,), daemon=True)
    generation_thread.start()

    check_generation_completion() # start monitoring the thread

def check_generation_completion():
    if generation_thread and generation_thread.is_alive():
        root.after(1000, check_generation_completion)
    else:
        show_done_label() # display "Done" when the generation completes

def show_done_label():
    status_label.config(text="Done", fg="green")
    root.after(5000, lambda: status_label.config(text="Ready", fg="green")) # set back to "Ready" after 5 seconds

def generate_tests_for_folder(model_name):
    global folder_path

    if not folder_path:
        print("No folder selected.")
        return

    prompt_text = tb_chosen_prompt_file.get("1.0", tk.END).strip()
    tests_folder = os.path.join(folder_path, "Tests")
    os.makedirs(tests_folder, exist_ok=True)

    py_files = [f for f in os.listdir(folder_path) if f.endswith(".py")]
    log_file_path = os.path.join(tests_folder, f"utg-{model_name}.log")

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        start_time = datetime.now()
        log_file.write(f"\n--- Test Generation Started ---\n")
        log_file.write(f"Model: {model_name}\n")
        log_file.write(f"Date: {start_time.strftime('%Y-%m-%d')}\n")
        log_file.write(f"Start Time: {start_time.strftime('%H:%M:%S')}\n")
        log_file.write(f"Folder: {folder_path}\n\n")

        py_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(generate_test_for_file, model_name, prompt_text, file, tests_folder, log_file): file
                for file in py_files
            }
            for future in concurrent.futures.as_completed(futures):
                filename = futures[future]
                try:
                    future.result()
                    print(f"Test generation completed for {filename}")
                    log_file.write(f"Completed: {filename} at {datetime.now().strftime('%M:%S')}\n")
                except Exception as e:
                    print(f"Error generating test for {filename}: {e}")
                    log_file.write(f"Error generating test for {filename}: {e}\n")

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        log_file.write(f"\n--- Test Generation Completed ---\n")
        log_file.write(f"End Time: {end_time.strftime('%H:%M:%S')}\n")
        log_file.write(f"Elapsed Time: {str(elapsed_time)}\n\n")

def generate_test_for_file(model_name, prompt_text, filename, tests_folder, log_file):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        code_text = file.read()

    full_prompt = f"{prompt_text}\n\n{code_text}\n"
    print(f"Generating test for {filename}...")

    stream = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': full_prompt}],
        stream=True,
    )

    generated_output = ""
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            generated_output += chunk['message']['content']

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

    base_filename = os.path.basename(os.path.splitext(filename)[0])
    test_filename = os.path.join(tests_folder, f"unit_test_{base_filename}_{model_name}.py")
    with open(test_filename, "w", encoding="utf-8") as test_file:
        test_file.write("\n".join(python_code_lines))

    log_file.write(f"Generated: {test_filename} for {filename} at {datetime.now().strftime('%H:%M:%S')}\n")

def check_ollama_status():
    ollama_running = any("ollama" in proc.name().lower() for proc in psutil.process_iter(['name']))
    if ollama_running:
        ollama_status_label.config(text="Online", fg="green")
    else:
        ollama_status_label.config(text="Offline", fg="red")
    root.after(5000, check_ollama_status)


# GUI setup
root = tk.Tk()
root.minsize(560, 420)
root.maxsize(560, 420)
root.title("Unit Test with AI")
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

frame_five = tk.Frame(main_frame)
frame_five.pack(side="top", padx=10, pady=10, fill="x")

status_label = tk.Label(frame_one, text="Ready", fg="green", font=("Arial", 12))
status_label.pack(side="left", anchor="w")

ollama_status_label = tk.Label(frame_one, text="Checking...", fg="orange", font=("Arial", 12))
ollama_status_label.pack(side="right", anchor="e")

lbl_chosen_folder = tk.Label(frame_two, text="Selected Folder:", fg="white", font=("Arial", 12))
lbl_chosen_folder.pack(pady=5, anchor="w")

tb_chosen_folder = tk.Text(frame_two, height=1.5, width=40, wrap="word")
tb_chosen_folder.pack(side="left")
tb_chosen_folder.config(state="disabled")

btn_folder = tk.Button(frame_two, text="Choose Folder with Python Files", command=chose_folder)
btn_folder.pack(side="left", padx=5)

lbl_chosen_prompt_file = tk.Label(frame_three, text="Prompt File:", fg="white", font=("Arial", 12))
lbl_chosen_prompt_file.pack(pady=5, anchor="w")

tb_chosen_prompt_file = tk.Text(frame_three, height=5, width=40, wrap="word")
tb_chosen_prompt_file.pack(side="left")
tb_chosen_prompt_file.config(state="disabled")

btn_prompt_file = tk.Button(frame_three, text="Choose Your Prompt File", command=chose_prompt_file)
btn_prompt_file.pack(side="left", padx=5)

lbl_model_select = tk.Label(frame_four, text="Select AI Model:", fg="white", font=("Arial", 12))
lbl_model_select.pack(pady=5, anchor="w")

combo_models = ttk.Combobox(frame_four, state="readonly", width=40)
combo_models['values'] = fetch_models()
combo_models.pack(side="left")
combo_models.bind("<<ComboboxSelected>>", on_model_select)

btn_generate = tk.Button(frame_five, text="Generate", command=generate_tests)
btn_generate.pack(side="top", pady=5, fill="x")

check_ollama_status()

root.mainloop()