import os


# Helper function to resolve paths and check scope
def _resolve_and_check_scope(working_directory, target_path_str):
    """
    Resolves the target_path_str relative to working_directory,
    and checks if the resolved path is within the working_directory's scope.
    Returns the absolute resolved path if valid, or an error string if out of scope.
    """
    abs_working_dir = os.path.abspath(working_directory)

    # Resolve target_path_str relative to abs_working_dir, then make it absolute
    combined_path = os.path.join(abs_working_dir, target_path_str)
    abs_resolved_path = os.path.abspath(combined_path)

    # Perform the "outside working directory" security check.
    if os.path.commonpath([abs_working_dir, abs_resolved_path]) != abs_working_dir:
        # **FIXED MESSAGE FOR CONSISTENCY**
        return f'Error: Cannot read "{target_path_str}" as it is outside the permitted working directory'

    return abs_resolved_path  # Return the valid absolute path.


# Main function for this assignment: Gets the content of a specified file.
def get_file_content(working_directory, file_path):
    # Step 1: Resolve the file_path relative to the working_directory and check scope.
    # The helper function handles initial path normalization and the 'outside working directory' check.
    resolved_path_or_error = _resolve_and_check_scope(working_directory, file_path)

    # **CRITICAL FIX HERE:**
    # Check if the helper function returned an ERROR string (one that starts with "Error:").
    if isinstance(resolved_path_or_error, str) and resolved_path_or_error.startswith(
        "Error:"
    ):
        return resolved_path_or_error  # Propagate the error immediately.

    # If it's not an error string, it must be the valid absolute path.
    resolved_file_full_path = resolved_path_or_error

    # Step 2: Verify that the resolved path actually points to a regular file.
    if not os.path.isfile(resolved_file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Step 3: Read the file content, with truncation and error handling.
    MAX_CHARS = 10000
    file_content_string = ""

    try:
        with open(resolved_file_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        actual_file_size = os.path.getsize(resolved_file_full_path)

        if actual_file_size > MAX_CHARS:
            file_content_string += (
                f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )

    except OSError as e:
        return f'Error: Could not read file "{file_path}": {e}'

    # Step 4: Return the file's content (potentially truncated).
    return file_content_string
