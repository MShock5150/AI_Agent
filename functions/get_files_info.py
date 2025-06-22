import os


def get_files_info(working_directory, directory=None):
    # Set base variables
    # Ensure working_directory is absolute from the start, as this defines the permission root.
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = None

    # Determine the absolute path of the target directory to list.
    # If 'directory' is None, it implies listing the 'working_directory' itself.
    if directory is None:
        abs_target_dir = abs_working_dir
    else:
        combined_path = os.path.join(abs_working_dir, directory)
        abs_target_dir = os.path.abspath(
            combined_path
        )  # Then normalize to absolute path

    # Check if target directory is outside the permitted working directory.
    # This uses os.path.commonpath to ensure that abs_target_dir is a subpath of abs_working_dir.
    if os.path.commonpath([abs_working_dir, abs_target_dir]) != abs_working_dir:
        # If it's outside, return a specific error message.
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # Check if the resolved target path exists and is actually a directory.
    elif not os.path.isdir(abs_target_dir):
        # If not a directory, return a specific error message.
        return f'Error: "{directory}" is not a directory'

    # If all initial checks pass, the abs_target_dir is valid and permitted.

    # Initialize contents list in case os.listdir fails.
    contents = []

    # Try to list the contents of the target directory.
    # This handles potential PermissionError, FileNotFoundError, etc., for the directory itself.
    try:
        contents = os.listdir(abs_target_dir)
    except OSError as e:
        return f'Error: Could not list directory "{directory}": {e}'

    # List to hold formatted strings for each item found.
    output_lines = []

    # Loop through each item (file or subdirectory name) in the contents list.
    for item_name in contents:
        # Try to get information for each individual item.
        # This handles errors if an item is deleted or permissions change mid-listing.
        try:
            # Construct the full absolute path to the current item.
            item_full_path = os.path.join(abs_target_dir, item_name)

            # Get the size of the item in bytes.
            item_size = os.path.getsize(item_full_path)

            # Check if the item is a directory.
            is_directory = os.path.isdir(item_full_path)

            # Format the item's information into the required string format.
            output_line = (
                f"- {item_name}: file_size={item_size} bytes, is_dir={is_directory}"
            )
            output_lines.append(output_line)
        except OSError as e:
            # If an error occurs for an individual item, return an error string
            # indicating which item caused the problem.
            return f'Error: Could not access item "{item_name}" in directory "{directory}": {e}'

    # Join all the formatted item strings with newlines to form the final output string.
    final_output_string = "\n".join(output_lines)

    return final_output_string

