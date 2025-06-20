import os
import sys

# Add the 'functions' directory to the Python path
# This allows us to import get_files_info directly by telling Python
# to look in the 'functions' subfolder within the current script's directory.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "functions"))
)

# Now, we can import the function since its containing directory is on the path
from get_files_info import get_files_info

# Determine the actual current working directory where the script is run from.
# This ensures consistency if you run the script from a different location than the project root.
current_project_root = os.getcwd()

print("--- Running Test Case 1: get_files_info(current_project_root, 'calculator') ---")
# Expected: Lists contents of the 'calculator' directory within the project root.
result1 = get_files_info(current_project_root, "calculator")
print(result1)
print("\n" + "=" * 50 + "\n")  # Separator for clear output

print(
    "--- Running Test Case 2: get_files_info(current_project_root, 'calculator/pkg') ---"
)
# Expected: Lists contents of the 'calculator/pkg' directory.
result2 = get_files_info(current_project_root, "calculator/pkg")
print(result2)
print("\n" + "=" * 50 + "\n")  # Separator

print("--- Running Test Case 3: get_files_info(current_project_root, '/bin') ---")
# Expected: Error: Cannot list "/bin" as it is outside the permitted working directory
# This tests the security boundary: attempting to access a system directory.
result3 = get_files_info(current_project_root, "/bin")
print(result3)
print("\n" + "=" * 50 + "\n")  # Separator

print("--- Running Test Case 4: get_files_info(current_project_root, '../') ---")
# Expected: Error: Cannot list "../" as it is outside the permitted working directory
# This tests attempting to access a parent directory from the project root.
result4 = get_files_info(current_project_root, "../")
print(result4)
print("\n" + "=" * 50 + "\n")  # Separator

# Optional Test Case 5: Test for a non-existent directory within bounds
print(
    "--- Running Test Case 5: get_files_info(current_project_root, 'non_existent_dir_in_root') ---"
)
# Expected: Error: "non_existent_dir_in_root" is not a directory
# This tests the 'is not a directory' check for a path that doesn't exist *relative to the root*.
result5 = get_files_info(current_project_root, "non_existent_dir_in_root")
print(result5)
print("\n" + "=" * 50 + "\n")  # Separator

# Optional Test Case 6: Test for a file instead of a directory within bounds
print("--- Running Test Case 6: get_files_info(current_project_root, 'tests.py') ---")
# Expected: Error: "tests.py" is not a directory
# This tests the 'is not a directory' check for a path that exists but is a file.
result6 = get_files_info(current_project_root, "tests.py")
print(result6)
print("\n" + "=" * 50 + "\n")  # Separator

# Optional Test Case 7: Test with directory=None (should list the working_directory itself)
print("--- Running Test Case 7: get_files_info(current_project_root, None) ---")
# Expected: Lists contents of the current_project_root itself.
result7 = get_files_info(current_project_root, None)
print(result7)
print("\n" + "=" * 50 + "\n")  # Separator
