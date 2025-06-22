import os


# Helper function to resolve paths and check scope for write operations.
# Copied and modified from get_file_content to tailor the error message.
def _resolve_and_check_scope(working_directory, target_path_str):
    """
    Resolves the target_path_str relative to working_directory,
    and checks if the resolved path is within the working_directory's scope.
    Returns the absolute resolved path if valid, or an error string if out of scope.
    """
    abs_working_dir = os.path.abspath(working_directory)

    combined_path = os.path.join(abs_working_dir, target_path_str)
    abs_resolved_path = os.path.abspath(combined_path)

    # **MODIFIED ERROR MESSAGE HERE FOR 'WRITE' CONTEXT**
    if os.path.commonpath([abs_working_dir, abs_resolved_path]) != abs_working_dir:
        return f'Error: Cannot write to "{target_path_str}" as it is outside the permitted working directory'

    return abs_resolved_path


def write_file(working_directory, file_path, content):
    # Use the helper function to resolve the path and perform the initial scope check.
    resolved_path_or_error = _resolve_and_check_scope(working_directory, file_path)

    # If the helper function returned an error string, propagate it immediately.
    if isinstance(resolved_path_or_error, str) and resolved_path_or_error.startswith(
        "Error:"
    ):
        return resolved_path_or_error

    # If we reach here, resolved_path_or_error is the valid absolute path to the file.
    # We'll assign it to a more descriptive variable for clarity.
    abs_file_full_path = resolved_path_or_error

    # Step 2: Implement file creation/overwrite logic within a try-except block.
    try:
        # Get the directory part of the absolute file path.
        # This is where the file will reside, and its parent directories might need to be created.
        file_directory = os.path.dirname(abs_file_full_path)

        # Check if the directory exists. If not, create it and all intermediate directories.
        # `exist_ok=True` prevents an error if the directory already exists.
        if not os.path.exists(file_directory):
            os.makedirs(file_directory, exist_ok=True)

        # Open the file in 'write' mode ("w").
        # This mode will create the file if it doesn't exist, or overwrite it if it does.
        # The 'with' statement ensures the file is properly closed after writing.
        with open(abs_file_full_path, "w") as f:
            f.write(content)  # Write the provided content to the file.

        # If the write operation was successful, return the specified success message.
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    # Catch any OSError (e.g., PermissionError, IOError) that might occur during directory creation or file writing.
    except OSError as e:
        # Return a specific error message indicating the file and the nature of the error.
        return f'Error: Could not write to file "{file_path}": {e}'
