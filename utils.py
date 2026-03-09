import os, re
import sys
import shutil
import platform
import tiktoken
import subprocess



def _find_pdflatex() -> str:
    """
    Resolve the pdflatex binary path.
    - On macOS, checks common MacTeX/TeXShop install locations if not on PATH.
    - On all platforms, falls back to 'pdflatex' and lets the OS raise the error.
    """
    # First try: already on PATH (works on Linux, CI, and macOS if ~/.zshrc exports it)
    found = shutil.which("pdflatex")
    if found:
        return found

    # Second try: macOS-specific known locations (MacTeX via TeXShop or standalone)
    if platform.system() == "Darwin":
        macos_candidates = [
            "/Library/TeX/texbin/pdflatex",           # MacTeX 2021+ default symlink dir
            "/usr/local/texlive/2024/bin/universal-darwin/pdflatex",
            "/usr/local/texlive/2023/bin/universal-darwin/pdflatex",
            "/usr/local/texlive/2024/bin/arm64-darwin/pdflatex",  # Apple Silicon
            "/usr/local/texlive/2023/bin/arm64-darwin/pdflatex",
            "/usr/texbin/pdflatex",                   # Legacy MacTeX location
        ]
        for candidate in macos_candidates:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate

    # Final fallback: let subprocess raise a clear FileNotFoundError
    return "pdflatex"


def compile_latex(latex_code, compile=True, output_filename="output.pdf", timeout=30):
    latex_code = latex_code.replace(
        r"\documentclass{article}",
        "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{array}\n\\usepackage{algorithm}\n\\usepackage{algorithmicx}\n\\usepackage{algpseudocode}\n\\usepackage{booktabs}\n\\usepackage{colortbl}\n\\usepackage{color}\n\\usepackage{enumitem}\n\\usepackage{fontawesome5}\n\\usepackage{float}\n\\usepackage{graphicx}\n\\usepackage{hyperref}\n\\usepackage{listings}\n\\usepackage{makecell}\n\\usepackage{multicol}\n\\usepackage{multirow}\n\\usepackage{pgffor}\n\\usepackage{pifont}\n\\usepackage{soul}\n\\usepackage{sidecap}\n\\usepackage{subcaption}\n\\usepackage{titletoc}\n\\usepackage[symbol]{footmisc}\n\\usepackage{url}\n\\usepackage{wrapfig}\n\\usepackage{xcolor}\n\\usepackage{xspace}")

    dir_path = "research_dir/tex"
    tex_file_path = os.path.join(dir_path, "temp.tex")
    with open(tex_file_path, "w") as f:
        f.write(latex_code)

    if not compile:
        return "Compilation successful"

    pdflatex = _find_pdflatex()

    try:
        result = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "temp.tex"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=dir_path
        )
        return f"Compilation successful: {result.stdout.decode('utf-8')}"

    except FileNotFoundError:
        return (
            "[CODE EXECUTION ERROR]: pdflatex not found. "
            f"Searched PATH and macOS TeX locations. "
            f"Ensure MacTeX is installed (https://www.tug.org/mactex/) "
            f"or add /Library/TeX/texbin to your PATH. "
            f"Resolved binary: '{pdflatex}'"
        )
    except subprocess.TimeoutExpired:
        return "[CODE EXECUTION ERROR]: Compilation timed out after {} seconds".format(timeout)
    except subprocess.CalledProcessError as e:
        return (
            f"[CODE EXECUTION ERROR]: Compilation failed: "
            f"{e.stderr.decode('utf-8')} {e.output.decode('utf-8')}. "
            f"There was an error in your latex."
        )


def count_tokens(messages, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    num_tokens = sum([len(enc.encode(message["content"])) for message in messages])
    return num_tokens

def remove_figures():
    """Remove a directory if it exists."""
    for _file in os.listdir("."):
        if "Figure_" in _file and ".png" in _file:
            os.remove(_file)

def remove_directory(dir_path):
    """Remove a directory if it exists."""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path)
            print(f"Directory {dir_path} removed successfully.")
        except Exception as e:
            print(f"Error removing directory {dir_path}: {e}")
    else:
        print(f"Directory {dir_path} does not exist or is not a directory.")


def save_to_file(location, filename, data):
    """Utility function to save data as plain text."""
    filepath = os.path.join(location, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(data)  # Write the raw string instead of using json.dump
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")


def clip_tokens(messages, model="gpt-4", max_tokens=100000):
    enc = tiktoken.encoding_for_model(model)
    total_tokens = sum([len(enc.encode(message["content"])) for message in messages])

    if total_tokens <= max_tokens:
        return messages  # No need to clip if under the limit

    # Start removing tokens from the beginning
    tokenized_messages = []
    for message in messages:
        tokenized_content = enc.encode(message["content"])
        tokenized_messages.append({"role": message["role"], "content": tokenized_content})

    # Flatten all tokens
    all_tokens = [token for message in tokenized_messages for token in message["content"]]

    # Remove tokens from the beginning
    clipped_tokens = all_tokens[total_tokens - max_tokens:]

    # Rebuild the clipped messages
    clipped_messages = []
    current_idx = 0
    for message in tokenized_messages:
        message_token_count = len(message["content"])
        if current_idx + message_token_count > len(clipped_tokens):
            clipped_message_content = clipped_tokens[current_idx:]
            clipped_message = enc.decode(clipped_message_content)
            clipped_messages.append({"role": message["role"], "content": clipped_message})
            break
        else:
            clipped_message_content = clipped_tokens[current_idx:current_idx + message_token_count]
            clipped_message = enc.decode(clipped_message_content)
            clipped_messages.append({"role": message["role"], "content": clipped_message})
            current_idx += message_token_count
    return clipped_messages



def extract_prompt(text, word):
    code_block_pattern = rf"```{word}(.*?)```"
    code_blocks = re.findall(code_block_pattern, text, re.DOTALL)
    extracted_code = "\n".join(code_blocks).strip()
    return extracted_code

def build_task_note(task_note, **kwargs):
    # Replace the `{{variable}}` placeholders in the task note with the provided values
    for note in task_note:
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            note["note"] = note["note"].replace(placeholder, str(value))
    return task_note

def remove_thinking_process(text):
    """
    Remove the first occurrence of a substring enclosed in <thinking>...</thinking> or <think>...</think>,
    even if it spans multiple lines.
    """
    pattern = r'<(?:thinking|think)>.*?</(?:thinking|think)>'
    # Using re.DOTALL allows '.' to match newline characters.
    return re.sub(pattern, '', text, count=1, flags=re.DOTALL)

# Define allowed phases and variables according to your guide
ALLOWED_PHASES = [
    "literature review", "plan formulation",
    "data preparation", "running experiments",
    "results interpretation", "report writing",
    "report refinement"
]

ALLOWED_VARIABLES = {
    "research_topic", "api_key", "deepseek_api_key",
    "google_api_key", "anthropic_api_key", "language",
    "llm_backend"
}

def validate_task_note_config(task_note_config):
    """
    Validate the task note configuration based on the allowed phases and variables.
    """
    # Ensure the configuration is a list
    if not isinstance(task_note_config, list):
        raise ValueError("Configuration must be a list.")

    for idx, note in enumerate(task_note_config):
        # Each note should be a dictionary
        if not isinstance(note, dict):
            raise ValueError(f"Entry {idx} must be a dictionary.")

        # Must contain both 'phases' and 'note'
        if "phases" not in note or "note" not in note:
            raise ValueError(f"Entry {idx} must have both 'phases' and 'note' keys.")

        # Validate phases: it must be a list and contain only allowed values
        phases = note["phases"]
        if not isinstance(phases, list):
            raise ValueError(f"'phases' in entry {idx} must be a list.")
        for phase in phases:
            if phase not in ALLOWED_PHASES:
                raise ValueError(
                    f"Invalid phase '{phase}' in entry {idx}. "
                    f"Allowed phases are: {ALLOWED_PHASES}"
                )

        # Validate note: it must be a string
        text = note["note"]
        if not isinstance(text, str):
            raise ValueError(f"'note' in entry {idx} must be a string.")

        # Validate the variables inside the note using a regex that matches double curly braces
        variables_found = re.findall(r"{{\s*(\w+)\s*}}", text)
        for var in variables_found:
            if var not in ALLOWED_VARIABLES:
                raise ValueError(
                    f"Invalid variable '{var}' in note in entry {idx}. "
                    f"Allowed variables are: {ALLOWED_VARIABLES}"
                )

    return True
