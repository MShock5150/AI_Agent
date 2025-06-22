import os
import sys

# Add the 'functions' directory to the Python path
# This allows us to import run_python_file directly
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "functions"))
)

# Import the new run_python_file function
from run_python import run_python_file

# Determine the actual current working directory where the script is run from.
# For most tests, this will be the agent's base.
current_project_root = os.getcwd()

print(
    "--- Running Test Case 1: run_python_file(current_project_root, 'calculator/main.py') ---"
)
# Expected: Runs calculator/main.py. Should print usage or a calculated result if arguments were passed (none here).
# This tests a valid Python file execution within the permitted working directory.
result1 = run_python_file(current_project_root, "calculator/main.py")
print(result1)
print("\n" + "=" * 50 + "\n")  # Separator for clear output

print(
    "--- Running Test Case 2: run_python_file(current_project_root, 'calculator/tests.py') ---"
)
# Expected: Runs calculator/tests.py. Should output whatever that script prints (likely nothing if it's empty).
# This tests another valid Python file execution within a nested path.
result2 = run_python_file(current_project_root, "calculator/tests.py")
print(result2)
print("\n" + "=" * 50 + "\n")  # Separator

# --- CRITICAL FIX FOR TEST CASE 3 ---
# This test specifically aims to check if the agent, *when its working_directory is 'calculator'*,
# can prevent execution of a file accessed by traversing *outside* that 'calculator' directory.
print(
    "--- Running Test Case 3: run_python_file('calculator', '../main.py') (Outside Permitted Dir) ---"
)
# Expected: Error: Cannot execute "../main.py" as it is outside the permitted working directory.
# This crucial test verifies the security boundary for paths that attempt to navigate outside the scope.
result3 = run_python_file(
    "calculator", "../main.py"
)  # <-- Changed first argument to "calculator"
print(result3)
print("\n" + "=" * 50 + "\n")  # Separator

print(
    "--- Running Test Case 4: run_python_file(current_project_root, 'calculator/nonexistent.py') (File Not Found) ---"
)
# Expected: Error: File "calculator/nonexistent.py" not found.
# This tests the check for a non-existent file path.
result4 = run_python_file(current_project_root, "calculator/nonexistent.py")
print(result4)
print("\n" + "=" * 50 + "\n")  # Separator
