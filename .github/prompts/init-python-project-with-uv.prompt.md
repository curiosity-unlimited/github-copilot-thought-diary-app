---
mode: 'agent'
tools: ['codebase', 'editFiles', 'runCommands']
description: 'Initialize a Python project using [uv](https://docs.astral.sh/uv/) and pin a specific Python version provided by the user.'
---

# Instructions
- I'm iterating this prompt to make it perfect. Please start from the beginning and reset any variable every time I run it.
- Please follow the steps below, step by step, and do not skip any of them. No more, no less.

## STEP 1: Check uv installation
Please check whether uv is installed in current environment by running `which uv`. If not, skip all the following steps and return "uv is not installed, please follow official documentation to install it, https://docs.astral.sh/uv/getting-started/installation/".

## STEP 2: Install a Python version provided by the user
Please ask user to specify the Python version to use for this project (3.11 or above, e.g., 3.12, 3.13, etc.):
<python_version>
Run the command `uv python install <python_version>` to install the specified Python version.

## STEP 3: Pin the installed Python version to the project
Run the command `uv python pin <python_version>` to pin the installed Python version to the project.

## STEP 4: Initialize a new Python project
Run the command `uv init .` to initialize a new Python project.

## STEP 5: Create a virtual environment
Run the command below to create a virtual environment using the pinned Python version:
```bash
uv venv --python <python_version> --clear
```

## STEP 6: Activate the virtual environment
Run the command below to activate the virtual environment:
```bash
source .venv/bin/activate
```

## STEP 7: Ensure `.gitignore` file exists
Check if a `.gitignore` file exists in the project root directory. If it does not exist, create an empty one.

## STEP 8: Use `.env` file to manage environment variables
1. Install the `python-dotenv` package to load environment variables from the `.env` file. Run the command:
```bash
uv add python-dotenv
```
2. Create a `.env` file in the project root directory to manage environment variables.
3. Add the following example content to the `.env` file:
```env
SECRET_KEY=your_secret_key
```
4. Load those environment variables from the `.env` file in `main.py` as an initial example.

## STEP 9: Generate `.gitignore` file content based on the project structure and best practices
- Please reference [.gitignore templates for Python](https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore) from [GitHub's official repository](https://github.com/github/gitignore) for best practices, and generate `.gitignore` file content based on the project #codebase as well as those best practices, while keeping specified files and folders tracked by git. Take `.vscode/` for example, following content should be generated in the `.gitignore` file (just comment out the entries, instead of using exclamation marks):
```markdown
# IDEs
# .vscode/
```
- Follow the example above and make sure to keep all the following list of files and folders tracked by git, and please **MERGE** duplicated entries into [.gitignore templates for Python](https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore) if any:  
    - `.python-version`
    - `uv.lock`
    - `.vscode/`
- By **MERGE**, I mean if an entry already exists in the template, just keep it as is without adding a duplicate entry. For example, if `.python-version` already exists in the template, do not add another `.python-version` entry again, nor should you just append it to the end of the file. Just keep the existing one as is.