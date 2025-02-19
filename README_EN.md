# AI-Unit-Testing

<p>English Version</p>

<hr>

## Table of Content

01. [Motivation](#motivation)
02. [Installation](#installation)
03. [Usage](#usage)
04. [Example](#example)
05. [Code](#code)
06. [Troubleshooting](#troubleshooting)
07. [Ollama](#ollama)
08. [Contributing](#contributing)
09. [Licence](#licence)
10. [Version](#version)

<hr><hr>

## 1. Motivation
- <p>This project was created as part of my bachelor's thesis at HFU Furtwangen. The aim is to use various AI models (open source) to determine which model works best and with which prompt the models can best create tests. The thesis aims to evaluate unit tests using AI, but can be manipulated by the prompts or other types of tests can be used.</p>
- <p>As software is becoming increasingly complex, larger and more confusing, my motivation was to automate the testing process. By developing a tool with Python, I tried to get a little closer to this step. AI has led to innovations that also have an impact on software development and can expand the testing process and further reduce software errors as far as possible.</p>

<hr>

## 2. Installation
- Download this GitHub repository with the command `git clone https://github.com/beri336/AI-Unit-Testing`
- Install all dependencies with `pip install ollama psutil`
- open the folder in your IDE and run it
    - or with `python main.py`
    - or create an executable program:

> for MacOS
- install py2app with `pip install py2app`.
- create a file named `setup.py` in the directory and add the following:

```Python
from setuptools import setup

APP = ['main.py']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```
- and now create the executable app from the setup.py with `python setup.py py2app`.
- the app is now in the `dist` folder

<br>

> for Windows and Linux
- install pyinstaller with `pip install pyinstaller`.
- create an executable programme with `pyinstaller --onefile main.py`.

<hr>

## 3. Usage
- run the program, the GUI looks like this:

![GUI](Pictures/GUI.png)

- click on the `Choose Folder` and select your Python project
- if you have a folder, such as a virtual development environment venv, this can be excluded in the `Choose Excluded Folder`
- if a "prompt"{.md, .txt, .doc} is present, it will be automatically inserted into the TextArea
    - if there is none, it can be selected manually with `Choose Prompt`
    - or write the prompt into the TextArea yourself
- in `Select AI Model`, select the AI model with which the unit test is to be created
- click on `Generate` to start the test generation

<hr>

## 4. Example
> <span style="color:orange;font-weight:500">After you have followed the steps from [Usage](#usage), the program looks like this:</span>

![Starting Generation](<Pictures/Starting Generation.png>)

- A total of 5 Python files were found
- The folder `Project 1` was selected and the sub-folder `Venv` was excluded from the generation
- A prompt file was found and automatically loaded
- `Deepseek-Coder-V2` was selected as AI model

- At the top left is the status label of the test process
    - `Ready`: no test process running, test generation can be started
    - `Generating, please wait... (x/y)`: the unit tests are being generated, where x represents the current number of completed tests and y represents the number of tests to be generated
    - `Done`: the unit tests have been generated and more can be created if required
- The Ollama status label is at the top right
    - <span style="color:green;font-weight:500">Ollama Online</span>: indicates that Ollama is running and the AI models can be accessed
    - <span style="color:red;font-weight:500">Ollama Offline</span>: indicates that Ollama is not running and no AI model is available

<br>

![While Generating](<Pictures/While Generating.png>)

- During test generation, the bracket and the progress bar show how far the test has progressed
- At the beginning it takes a little longer, as the AI model has to be started and addressed, and depending on the lines of code and complexity, the generation can take longer

<br>

![Done Generating](<Pictures/Done Generating.png>)

- The generation of all tests is complete, the status label shows `Done` and the progress bar is reset to the default `0`

<br>

![Ollama Offline](<Pictures/Ollama Offline.png>)

- If `Ollama Offline` is displayed, it means that Ollama is not running on your system
- Open the terminal and start Ollama, every 10 seconds the program checks whether Ollama is active and then displays it

<hr>

## 5. Code
> <span style="color:orange;font-weight:500">This section briefly explains what the respective functions do</span>

> `terminal_debugging(...)`, `terminal_standard(...)` and `terminal_error(...)`
- displays print output in colour in the console

<br>

> `chose_folder()`
- opens a `file dialog`, where the user can select his folder
- if prompt [`‘txt’, ‘md’, ‘doc’`] is found, it is loaded into the text field

<br>

> `chose_exclude_folder()`
- if the main directory has been selected, the exclude button becomes clickable, otherwise it remains greyed and unclickable
- only sub-folders of the main directory can be selected
- only one sub-folder can be selected (for example a `virtual development environment`)

<br>

> `chose_prompt_file()`
- if no prompt file was found, the user can use this to select a file

<br>

> `fetch_models()`
- uses the `subprocess` to execute `ollama list` in the terminal
- the result is filtered by the model name, as only the name is necessary for the program
- if a cache of the model names is available, it will be used

<br>

> `on_model_select(...)`
- when the user selects an AI model from the list, this function update the variable and the `Generate` button

<br>

> `initialize_progress_bar(...)`
- if Python files are found, this function sets the total number to 100% for the progress bar

<br>

> `update_progress_bar(...)`
- when a test of the total number is completed, this function updates the progress bar

<br>

> `reset_progress_bar()`
- When all tests have been completed, this function resets the progress bar to `0`

<br>

> `generate_tests()`
- if no model has been selected, the test process will not start
- searches for all `*.py` files in the folder and saves their path
- if no files are found, an error is displayed in the terminal
- opens a new thread and starts the function `generate_tests_for_folder()`
- also starts the function `check_generation_completion()`

<br>

> `check_generation_completion()`
- checks every second whether the thread from `generate_tests()` is running
- if not, all tests are completed and the function `show_done_label()` will start

<br>

> `show_done_label()`
- updates the status label to `Done` and sets the label back to `Ready` after 5 seconds

<br>

> `generate_tests_for_folder(...)`
- creates a `Tests` folder in the main directory
- creates a log file with unit test generation details
- for every single Python file `generate_test_for_file()` is called
- starts `reset_progress_bar()`

<br>

> `generate_test_for_file(...)`
- sends every single Python file to the selected AI model, intercepts the Markdown query and filters it only for the Python code and removes the rest
- adds the generation time to the log file

<br>

> `check_ollama_status()`
- checks every 10 seconds whether Ollama is still active

<br>

> Structure of the GUI
- sets `minsize` and `maxsize` to the exact X- and Y-coordinates to fix the GUI
- creates a main frame
- creates further sub-frames within the main frame:
    - `frame one` displays the test status and Ollama status
    - `frame two` shows the selected main folder
    - `frame three` shows the excluded folder within the main folder
    - `frame four` shows the prompt
    - `frame five` shows all selectable AI models
    - `frame six` shows the `Generate` button
    - `frame seven` shows the progress bar

<hr>

## 6. Troubleshooting
- The performance of the program depends on the selected AI model. In some cases, the test process can take a few seconds, but it can also take several minutes.
- The performance also depends on the given code (simple, complex, only a few lines of code or several 1,000 lines).
- Performance varies from system to system. With better GPUs, generation is faster.
- As errors cannot be ruled out, it is advisable to look at the generated unit tests again. AI makes mistakes.

<hr>

## 7. Ollama
> What is Ollama?
- Ollama is a lightweight framework that allows you to run large language models (LLMs) locally on your system.
- It provides a simple API that can be used to create, execute and manage models.
- There is also a library of ready-made and pre-trained models that can be used in various applications.
- With Ollama, models such as LLama 3.2, Phi 3, Gemma 2 or others can be used and even customised or created.
- This tool is available for all common operating systems (macOS, Linux, Windows) and can be downloaded [here](https://ollama.com/download).
- The huge advantage of the local version is that no personal data is sent to third parties.
- Ollama also offers a REST API, which facilitates integration into other applications.
- Official Docker images are also available from Ollama, which simplifies the containerised environment.
- It also offers libraries in programming languages so that they can be easily integrated into the program code: [here for Python on GitHub](https://github.com/ollama/ollama-python).

<br>

> How can I download Ollama?
- Go to the [official homepage of Ollama](https://ollama.com) or directly to the [download website](https://ollama.com/download).
- Now install Ollama for your operating system.

<br>

> How can I download AI models with Ollama?
- Downloading models couldn't be easier.
- Go to the [official Ollama model list](https://ollama.com/search) and select your AI model.
- The following models were used in this project:
    - [LLama3.2](https://ollama.com/library/llama3.2:3b)
    - [Gemma2](https://ollama.com/library/gemma2:9b)
    - [Deepseek Coder V2](https://ollama.com/library/deepseek-coder-v2:16b)
    - [CodeGemma](https://ollama.com/library/codegemma:7b)

<br>

> Quick tour through Ollama
- <span style="color:orange;font-weight:500">All of the following commands must be executed in the terminal.</span>

>> Download AI models: `ollama pull {your-ai-model}`
>>> if you want to download a special variant (parameter): `ollama pull {your-ai-model}:{parameter}`

>> Start AI model: `ollama run {your-ai-model}`

>> Show all downloaded AI models: `ollama list`

>> Show information about the AI model: `ollama show {dein-ai-modell}`

>> Start Ollama: `ollama serve`

>> Terminate AI-Modell: `ollama stop {dein-ai-modell}`

>> Show all currently running AI models: `ollama ps`

>> For more: `ollama --help`

<hr>

## Contributors
- Berkant Simsek (Creator)

<hr>

## Licence
- MIT Licence

<hr>

## Version
> `V1.0`
- Automated Unit-Test-Generation using AI.

<hr>