import subprocess # Run system commands (fetch AI models from terminal)

model_names_cache = None # Cache as a global variable so that it remains saved

# Logging-Funktion
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

# Ollama functionality
def fetch_models(gui_instance):
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
    if model_names_cache is not None: # Prevents the cache from being overwritten again and again
        output_terminal("Info #11: Using cached model list.", "green")
        return model_names_cache
        
    try:
        # Execute the command `ollama list` to load models from the terminal
        output_terminal("Info #12: Fetching available AI models...", "green")

        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)

        # Process the terminal output: Extract only the model names (first column of the output)
        model_names = [line.split()[0] for line in result.stdout.splitlines() if not line.startswith("NAME")]

        # Save the models in the cache to avoid repeated queries
        model_names_cache = model_names

        output_terminal(f"Info #13: Available AI models: {', '.join(model_names)}", "green")

        return model_names
    
    except FileNotFoundError as e:
        # Error handling if ollama is not installed on OS
        gui_instance.set_ollama_label("PathError")
        output_terminal(f"Error #14: Ollama not found! Make sure Ollama is installed and added to the system PATH. - {e}", "bg_red")
        return [] # Fallback: Return of an empty list

    except subprocess.CalledProcessError as e:
        # Error handling if `ollama list` fails
        output_terminal(f"Error #7: Failed to fetch models using 'ollama list': {e}", "bg_red")
        return [] # Fallback: Return of an empty list
